import logging
import os
import json
import discord
from discord.utils import find
from discord.ext import commands

# logger stuff yeah
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER_HANDLER = logging.FileHandler(
    filename="logs/{}.log".format(__name__), encoding='utf-8', mode='w')
LOGGER_HANDLER.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(LOGGER_HANDLER)

thingy = os.path.dirname(os.path.abspath(__file__))
nagisa = os.path.join(thingy, "../config/taiga.json")

with open(nagisa) as file:
    data = json.load(file)
    role_name = data["stream_role"]


# really messy

class OnStream:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_update(self, before, after):
        guild = after.guild
        channel = guild.default_channel
        role = find(lambda m: m.name == role_name, guild.roles)
        mention = after.mention
        if role is None:
            try:
                await guild.create_role(name=role_name,
                                        hoist=True,
                                        colour=discord.Colour.purple())
                role = find(lambda m: m.name == role_name, guild.roles)
            except:
                pass
        try:
            if after.game.type == 1:
                em = discord.Embed(title="Stream Notification",
                                   description="{} is now streaming!".format(
                                       mention),
                                   colour=discord.Colour.purple())
                em.add_field(name="URL:", value=after.game.url)
        except:
            pass

        if after.game is not None:
            game_type = after.game.type
        else:
            game_type = 0

        if before.game is not None:
            before_game_type = before.game.type
        else:
            before_game_type = 0

        if game_type == 1 and role not in after.roles and before_game_type != 1:
            try:
                await channel.send(embed=em)
                await after.add_roles(role)
            except discord.Forbidden as exc:
                error = "{} has thrown an exception:\n{}".format(__name__, exc)
                msg = "Probably not enough permissions."
                LOGGER.error(error)
                LOGGER.error(msg)
                print(error)
                print(msg)
        elif game_type != 1 and role in after.roles and before_game_type == 1:
            await after.remove_roles(role)
            em2 = discord.Embed(title="Stream Notification",
                                description="{} is no longer streaming.".format(
                                    mention),
                                colour=discord.Colour.purple())
            await channel.send(embed=em2)



def setup(bot):
    bot.add_cog(OnStream(bot))
