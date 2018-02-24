import json
import os

import discord
from discord.ext import commands

thingy = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(thingy, "../config/auto_roles.json")


class Moderation_Helper:
    """moderation helper cog class"""

    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        with open(config, encoding='utf8') as file:
            data = json.load(file)

        if data[str(member.guild.id)] is not None:
            try:
                role = discord.utils.get(
                    member.guild.roles, name=data[str(member.guild.id)])
                await member.add_roles(role)
            except discord.Forbidden:
                print("Missing Permissions to add role {}.").format(
                    data[str(member.guild.id)])


def setup(bot):
    bot.add_cog(Moderation_Helper(bot))
