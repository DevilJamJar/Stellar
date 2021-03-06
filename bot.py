import asyncio
import json
import os

import discord
from discord.ext import commands

from subclasses import intents, StellarColour, StellarContext, StellarEmbed

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"


def parsetoken():
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data['token']


class Bot(commands.AutoShardedBot):
    def __init__(self, event_loop):
        super().__init__(command_prefix=self.get_prefix, intents=intents, case_insensitive=True,
                         loop=event_loop, description="**__The intra-space economy bot!__**")
        self.colour = StellarColour
        self.color = StellarColour
        self.Embed = StellarEmbed

        for filename in os.listdir('cogs'):
            if filename.endswith('.py') and filename != 'secrets.py':
                self.load_extension('cogs.{}'.format(filename[:-3]))
        self.load_extension('jishaku')

    async def get_prefix(self, message: discord.Message) -> str:
        with open('guildconfig.json', 'r') as f:
            prefixes = json.load(f)
        try:
            guild_prefix = prefixes[str(message.guild.id)]["prefix"]
        except KeyError:
            guild_prefix = 'st+'
        return commands.when_mentioned_or(guild_prefix)(self, message)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or StellarContext)

    async def on_ready(self) -> None:
        print('\n')
        print(f'Logged in as: {self.user.name}#{self.user.discriminator}')
        print(f'With ID: {self.user.id}\n——————————————————————————————')
        await self.change_presence(activity=discord.Activity(type=5, name="an intra-space battle"))
        print(f'Status changed successfully\n——————————————————————————————')

    def run(self):
        super().run(parsetoken())
