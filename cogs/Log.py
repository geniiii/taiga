import os
import json
import datetime

import discord
from discord.ext import commands

thingy = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(thingy, "config/logging.json")


class Logging:
    """logging cog class"""

    def __init__(self, bot):
        self.bot = bot
        with open(config, encoding='utf8') as file:
            data = json.load(file)
        self.channel_name = data["channel"]
        self.mod_channel_name = data["mod_channel"]
        self.join_title = data["join_title"]
        self.join_msg = data["join_msg"]
        self.leave_title = data["leave_title"]
        self.leave_msg = data["leave_msg"]
        self.ban_title = data["ban_title"]
        self.ban_msg = data["ban_msg"]
        self.unban_title = data["unban_title"]
        self.unban_msg = data["unban_msg"]

    async def on_member_join(self, member):
        channel = discord.utils.get(
            member.guild.text_channels, name=self.channel_name)

        if channel is None:
            return

        timestamp = datetime.datetime.now()
        timestamp.strftime('%H:%M:%S, %d (%A) %B %Y')
        timestamp = timestamp.replace(microsecond=0)

        on_join_embed = discord.Embed(title=self.join_title.format(member.name),
                                      description=self.join_msg.format(
                                          member.name),
                                      color=discord.Colour.green())
        on_join_embed.set_footer(text="Join Notification ({}) | {}".format(len(member.guild.members), timestamp),
                                 icon_url=member.avatar_url)

        await channel.send(embed=on_join_embed)

    async def on_member_remove(self, member):
        channel = discord.utils.get(
            member.guild.text_channels, name=self.channel_name)

        if channel is None:
            return

        timestamp = datetime.datetime.now()
        timestamp.strftime('%H:%M:%S, %d (%A) %B %Y')
        timestamp = timestamp.replace(microsecond=0)

        on_join_embed = discord.Embed(title=self.leave_title.format(member.name),
                                      description=self.leave_msg.format(
                                          member.name),
                                      color=discord.Colour.red())
        on_join_embed.set_footer(text="Leave Notification ({}) | {}".format(len(member.guild.members), timestamp),
                                 icon_url=member.avatar_url)

        await channel.send(embed=on_join_embed)

    async def on_member_ban(self, guild, member):
        channel = discord.utils.get(
            member.guild.text_channels, name=self.mod_channel_name)

        if channel is None:
            return

        timestamp = datetime.datetime.now()
        timestamp.strftime('%H:%M:%S, %d (%A) %B %Y')
        timestamp = timestamp.replace(microsecond=0)

        on_join_embed = discord.Embed(title=self.ban_title.format(member.name),
                                      description=self.ban_msg.format(
                                          member.name),
                                      color=discord.Colour.red())
        on_join_embed.set_footer(text="Ban Notification | {}".format(timestamp),
                                 icon_url=member.avatar_url)

        await channel.send(embed=on_join_embed)

    async def on_member_unban(self, guild, member):
        channel = discord.utils.get(
            guild.text_channels, name=self.mod_channel_name)

        if channel is None:
            return

        timestamp = datetime.datetime.now()
        timestamp.strftime('%H:%M:%S, %d (%A) %B %Y')
        timestamp = timestamp.replace(microsecond=0)

        on_join_embed = discord.Embed(title="**{}** has been unbanned from the server!".format(member.name),
                                      description="**{}** has been unbanned from the server!".format(
                                          member.name),
                                      color=discord.Colour.green())
        on_join_embed.set_footer(text="Unban Notification | {}".format(timestamp),
                                 icon_url=member.avatar_url)

        try:
            await channel.send(embed=on_join_embed)
        except:
            pass


def setup(bot):
    bot.add_cog(Logging(bot))
