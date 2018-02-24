"""experimental serverhub clone"""
import os
import json
from discord.ext import commands
import discord


class ServerHub:
    def __init__(self, bot):
        self.bot = bot
        self.thingy = os.path.dirname(os.path.abspath(__file__))
        self.config = os.path.join(self.thingy, "config/serverhub.json")
        with open(self.config) as file:
            data = json.load(file)
            self.channel_name = data["channel_name"]

    async def on_message(self, msg):
        if msg.channel.name == self.channel_name and msg.author.id != self.bot.user.id:
            for channel in self.bot.get_all_channels():
                if channel.name == self.channel_name and channel != msg.channel:
                    if msg.attachments:
                        for attachment in msg.attachments:
                            if msg.author.name != msg.author.display_name:
                                name = "{}/{}".format(msg.author.name,
                                                      msg.author.display_name)
                            else:
                                name = msg.author.name
                            if msg.author.bot:
                                await channel.send("**{} (Bot)**: {}".format(name,
                                                                             msg.clean_content + attachment.url))
                            else:
                                await channel.send("**{}**: {}".format(name,
                                                                       msg.clean_content + attachment.url))
                    elif msg.attachments and msg.embeds:
                        for attachment in msg.attachments:
                            for embed in msg.embeds:
                                if msg.author.name != msg.author.display_name:
                                    name = "{}/{}".format(msg.author.name,
                                                          msg.author.display_name)
                                else:
                                    name = msg.author.name
                                if msg.author.bot:
                                    await channel.send("**{} (Bot)**: {}".format(name,
                                                                                 msg.clean_content + attachment.url), embed=embed)
                                else:
                                    await channel.send("**{}**: {}".format(name,
                                                                           msg.clean_content + attachment.url), embed=embed)
                    elif msg.embeds:
                        for embed in msg.embeds:
                            if msg.author.name != msg.author.display_name:
                                name = "{}/{}".format(msg.author.name,
                                                      msg.author.display_name)
                            else:
                                name = msg.author.name
                            if msg.author.bot:
                                await channel.send("**{} (Bot)**: {}".format(name,
                                                                             msg.clean_content), embed=embed)
                            else:
                                await channel.send("**{}**: {}".format(name,
                                                                       msg.clean_content), embed=embed)
                    else:
                        if msg.author.name != msg.author.display_name:
                            name = "{}/{}".format(msg.author.name,
                                                  msg.author.display_name)
                        else:
                            name = msg.author.name
                        if msg.author.bot:
                            await channel.send("**{} (Bot)**: {}".format(name,
                                                                         msg.clean_content))
                        else:
                            await channel.send("**{}**: {}".format(name,
                                                                   msg.clean_content))


def setup(bot):
    bot.add_cog(ServerHub(bot))
