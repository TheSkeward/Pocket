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
async def on_message(message):
    logging.info(message.author.name + " (" + message.author.id + ") said \"" + message.content + "\" in " + message.channel.name)

    if not message.author.id in ignore_list:
        await client.send_message(message.channel, message.content)

client.run("a_muse_ing@mail.com", "Amusement4Masses")
