#! py -3

import discord
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

client = discord.Client()

ignore_list = []

@client.event
async def on_ready():
    logging.info("Logged in as " + client.user.name + " (" + client.user.id + ")")
    ignore_list.append(client.user.id)              # Ignore self, or else Muse would respond to himself

@client.event
async def on_message(message: discord.Message):
    logging.info(message.author.name + " (" + message.author.id + ") said \"" + message.content + "\" in " + message.channel.name)

    # Ignore those to be ignored
    if not message.author.id in ignore_list:
        addressed = is_addressed(message)
        content = message.content
        if addressed:
            content = content[5:].strip()           # Remove the prefix ("muse," or "Muse:"), which is 5 chars long

        await client.send_message(message.channel, parse(message, content, addressed))


def is_addressed(message: discord.Message):
    """
    Determines if muse was addressed, ie "Muse, inspire me" or "muse: give me a suggestion"
    If he was addressed, returns the rest of the message. If not, then returns None
    """
    prefix = message.content.split()[0].lower()
    if prefix == "muse," or prefix == "muse:":
        return True
    return False

def parse(context: discord.Message, message: str, addressed: bool):
    """
    Parses the actual message, scanning for triggers and errata.
    Returns a reply - or None, if it is not to be.
    """
    return message


client.run("a_muse_ing@mail.com", "Amusement4Masses")
