# -*- coding: utf-8 -*-
# main.py

import os

from discord.ext import commands
import music

cogs = [music]

client = commands.Bot(command_prefix='$')
client.remove_command('help')

for i in range(len(cogs)):
    cogs[i].setup(client)

if __name__ == '__main__':
    token = os.getenv('TOKEN')
    client.run(token)
