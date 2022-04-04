# -*- coding: utf-8 -*-
# main.py

import os

from discord.ext import commands
import music


with open('BAD_WORDS.txt', 'r', encoding='UTF-8') as file:
    bad_words = file.read().split(', ')


cogs = [music]

client = commands.Bot(command_prefix='$')
client.remove_command('help')


@client.event
async def on_message(ctx):
    await client.process_commands(ctx)

    msg = ctx.content.lower()

    if msg in bad_words:
        await ctx.delete()
        await ctx.send(f'**{ctx.message.author}**, нахуя материшья? Охуел вообще, уебан жирный')


for i in range(len(cogs)):
    cogs[i].setup(client)


if __name__ == '__main__':
    token = os.getenv('TOKEN')
    client.run(token)
