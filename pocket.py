#! py -3

import discord
import asyncio
import sqlite3, random, re, string, time
import markdown, html.parser
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)

# initialize database if anything's missing from it.
import init_db

conn = sqlite3.connect("pocket.db")
c = conn.cursor()
client = discord.Client()

pocket_size = 20
class inventory():
    def size():
        c.execute("SELECT COUNT(*) FROM inventory LIMIT 1;")
        return int(c.fetchone()[0])
    def add(item: str):
        c.execute("INSERT INTO inventory (item) VALUES (?);", (item,))
        conn.commit()
    def pop() -> str:
        """
        Randomly removes and returns one of the items in inventory.
        """
        c.execute("SELECT id FROM inventory;")
        rand_id = random.choice(c.fetchall())[0]
        c.execute("SELECT item FROM inventory WHERE id=? LIMIT 1;", (rand_id,))
        popped_item = c.fetchone()[0]
        c.execute("DELETE FROM inventory WHERE id=?;", (rand_id,))
        conn.commit()
        return popped_item
    def list():
        c.execute("SELECT item FROM inventory;")
        return [item_tuple[0] for item_tuple in c.fetchall()]

class message_janitor(html.parser.HTMLParser):
    """
    Class to strip text out of HTML, to be used to strip the text out of the Markdown-turned-HTML.
    Make sure not to strip out HTML-looking markup, ie <reply>.
    """
    def __init__(self, message: str):
        super().__init__()
        self.reset()

        self.message = message
        self.replying = False
        self.sanitized = []

        # Start the sanitizing
        self.feed(markdown.markdown(message))
    def handle_starttag(self, tag, attrs):
        # Not very long-term if planning to add more attributes.
        if tag == "reply":
            self.sanitized.append("<reply>")
            self.replying = True
    def handle_data(self, data):
        if not self.replying:
            self.sanitized.append(data)
    def get_data(self):
        # If is a tidbit, then keep the markdown for the rest of the message.
        if "<reply>" in self.message:
            self.sanitized.append(self.message[self.message.index("<reply>") + 7:])
        return ''.join(self.sanitized)

@client.event
async def on_ready():
    logging.info("Logged in as " + client.user.name + " (" + client.user.id + ")")
    c.execute("INSERT OR IGNORE INTO ignore (ignoramous) VALUES (?);", (client.user.id,))       # Ignore self, or else Pocket would respond to himself
    conn.commit()

@client.event
async def on_message(message: discord.Message):
    logging.info(message.author.name + " (" + message.author.id + ") said \"" + message.content + "\" in " + str(message.channel))

    # Ignore those to be ignored
    c.execute("SELECT ignoramous FROM ignore WHERE ignoramous=?", (message.author.id,))
    if not c.fetchall():
        addressed, content = process_meta(message)
        response = respond(message, content.strip(), addressed)
        if response:                                # Only send_message if there is a response; most of the time, there won't be.  time.sleep(.5)
            await client.send_message(message.channel, populate(message, response))


def process_meta(message: discord.Message) -> (bool, str):
    """
    Determines if Pocket was directly addressed, ie "Pocket, inspire me" or "pocket: give me a suggestion"
    If he was addressed, returns true and the rest of the message. If not, then return false and the message.
    Cleans up the message, too.
    """
    # First remove the prefix if addressed.
    if message.content.lower().startswith("pocket,") or message.content.lower().startswith("pocket:"):
        response = [True, message.content[7:]]      # Remove the prefix ("pocket," or "Pocket:"), which is 7 chars long
    else: response = [False, message.content]

    # Then sanitize the input message.
    response[1] = sanitize_message(response[1])

    return tuple(response)

def sanitize_message(message: str) -> str:
    """
    Cleans up the message of markdown and end punctuation.
    """
    message = message_janitor(message).get_data()
    # Remove end punctuation
    for outlawed in "?!.":
        message.rstrip(outlawed)
    # Remove commas
    message = re.compile(",").sub('', message)

    return message

def respond(context: discord.Message, message: str, addressed: bool) -> str or None:
    """
    Parses the actual message, scanning for triggers and errata.
    Returns a reply - or None, if it is not to be.
    """
    response = ""

    # If Pocket was addressed, then it might be a command
    if addressed:
        # Check for commands
        response = process_commands(message)
        if response: return response

    # If here, then it's not a command. Check for triggers.
    response = process_triggers(message)
    if response: return response

    # If addressed but still don't have a response, say so.
    if addressed: return "<unknown>"
    else: return None

def process_commands(message: str) -> str or None:
    if "<reply>" in message:
        try:
            tidbit = [portion.strip() for portion in message.split("<reply>")]

            # Sanitize the trigger some
            tidbit[0] = tidbit[0].lower()       # Lowercase the trigger; it has to be case insensitive.
            if re.match('^pocket[:,]', tidbit[0]):
                tidbit[0] = tidbit[0][7:].strip()

            c.execute("INSERT OR FAIL INTO comments (triggers, remark, protected) VALUES (?, ?, 0);", tidbit)
            conn.commit()
        except sqlite3.IntegrityError as e:
            # If IntegrityError, Pocket already has this tidbit.
            return "I already had it that way, $who."
        return "Ok, $who. \"" + tidbit[0] + "\" triggers \"" + tidbit[1] + "\"."

    if message.startswith("literal "):
        c.execute("SELECT remark FROM comments WHERE triggers=?", (message[8:].lower(),))
        result = c.fetchall()
        if result:
            response = "\"" + message[8:].lower() + "\" triggers:\n"
            for remark in [result_tuple[0] for result_tuple in result]:
                response += " - \"" + remark + "\"\n"
        else: response = "\"" + message[8:].lower() + "\" doesn't trigger anything."
        return "<literal>" + response

    result = process_inventory_triggers(message, True)
    if result:
        return result

    return None

def process_triggers(message: str) -> str or None:
    c.execute("SELECT remark FROM comments WHERE triggers=?", (message.lower(),))
    result = c.fetchall()
    if result:
        return random.choice(result)[0]

    result = process_inventory_triggers(message, False)
    if result:
        return result

    return None

def process_inventory_triggers(message: str, addressed: bool) -> str or None:
    """
    Proccesses a message (both triggers and commmands) regarding the inventory.
    """
    # Prep the message for processing
    message = message.strip(".").strip("!")

    ### GIVE ITEM commands ###
    # Addressed commands
    addressed_give = [re.compile("(?:have|take) (.+)$", re.IGNORECASE)]
    # Non-addressed commands
    unaddressed_give = [re.compile("puts (.+) in pocket$", re.IGNORECASE),
                        re.compile("gives pocket (.+)$", re.IGNORECASE),
                        re.compile("gives (.+) to pocket$", re.IGNORECASE),
                        re.compile("(?:have|take) (.+), pocket$", re.IGNORECASE)]
    for command in unaddressed_give + addressed_give if addressed else unaddressed_give:
        given_thing = command.match(message)
        if given_thing:
            return inventory_add(given_thing.group(1))

    ### DROP ITEM commands ###
    # Addressed commands
    addressed_drop = [re.compile("drop something", re.IGNORECASE)]
    for command in addressed_drop:
        if command.match(message):
            return "<drop item>"

    ### LIST INVENTORY commands ###
    if re.compile("inventory").match(message):
        if inventory.size() > 1:
            response = "_Pocket contains "
            for item in inventory.list()[:-1]: response += (item + ", ")
            response += "and " + inventory.list()[-1] + "._"
            return response
        elif inventory.size() == 1:
            return "_contains " + inventory.list()[0] + "._"
        else: return "<inventory empty>"

    return None

def inventory_add(new_item: str) -> str:
    """
    Adds new_item to the inventory. If inventory full, or is a duplicate, doesn't add.
    Either way, returns with an appropriate response.
    """
    if not new_item in inventory.list():
        if not inventory.size() < pocket_size:
            inventory.add(new_item)
            response = "<replace item>"
        else:
            inventory.add(new_item)
            response = "<get item>"
    else: response = "<duplicate item>"

    if response: return response + new_item
    else: return None

def inventory_drop() -> str:
    """
    Removes a random item from inventory. If inventory is empty, return appropriate response.
    Returns dropped item or None
    """
    if not inventory.size() > 0: return None
    else:
        dropped = inventory.pop()
        return dropped

def populate(context: discord.Message, response: str) -> str:
    """
    Replaces variables in a response with values. ie $who with a random active user, or $item with a random item
    Replaces <command> with an appropriate variation
    """
    # Check for phrase shortcuts
    command_response = re.compile("^(<.+>)(.*)$", re.DOTALL).match(response)
    if command_response:
        # The unpopulated response flag
        if command_response.group(1) == "<literal>": return command_response.group(2) if len(command_response.groups()) > 1 else None

        c.execute("SELECT response FROM auto_responses WHERE command=?", (command_response.group(1),))
        result = c.fetchall()
        if result:
            response = random.choice(result)[0]
        else: raise ValueError(response + " is not a known command.")

        # Replace %received with the item received, if any.
        if "%received" in response:
            if len(command_response.groups()) > 1:
                response = response.replace("%received", command_response.group(2))
            else: raise ValueError("No %received value passed, as was expected.")


    ### Placeholder Operations ###

    # -- $who : replaces with the sender of the message
    response = response.replace("$who", context.author.name)

    # -- $someone : replaces with a random online user
    online_peeps = list(context.server.members) if context.server else [context.author]     # In case of PM
    response = response.replace("$someone", random.choice(online_peeps).name)

    # -- $item : replaces with a random item in the inventory, if there is one.
    if "$item" in response:
        item_drop = inventory_drop()

        # SPECIAL CASE: when replacing an item, need to ensure that the newly dropped item is not the same item
        if command_response:
            if len(command_response.groups()) > 1:
                if command_response.group(2) == item_drop:
                    # That is, if the new drop and the old add are the same, fix that.
                    item_drop = inventory_drop()        # Don't worry about no other items; if you're dropping and receiving, you're replacing, which means inventory is full
                    inventory_add(command_response.group(2))

        if item_drop: response = response.replace("$item", item_drop)
        else: return populate(context, "inventory empty")   # If empty, can't drop anything.

    return response if response else None


client.run("a_muse_ing@mail.com", "Amusement4Masses")
