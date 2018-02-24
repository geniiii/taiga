import json
import os
from discord.ext import commands
import discord

class OnJoin:
    def __init__(self, bot):
        self.bot = bot

        thingy = os.path.dirname(os.path.realpath('__file__'))

        config = os.path.join(thingy, "config/taiga.json")
        other_config = os.path.join(thingy, "config/config.json")

        with open(config, encoding='utf8') as exa:
            data = json.load(exa)
        self.join_title = data["join_title"]
        self.join_mess = data["join_message"]
        self.image = data["jm_image"]

        with open(other_config) as lol:
            data = json.load(lol)
        self.game = data["game"]

    async def on_guild_join(self, guild):
        channel = guild.default_channel
        url = self.image

        message = discord.Embed(title=self.join_title,
                                description=self.join_mess,
                                color=discord.Colour.green())
        message.set_image(url=url)

        await channel.send(embed=message)

        servers = str(len(self.bot.guilds))
        game = discord.Game(name=self.game.format(self.bot.command_prefix, servers))

        await self.bot.change_presence(game=game)


def setup(bot):
    """adds the cog as a cog"""
    bot.add_cog(OnJoin(bot))
