"""Announcment commands."""
import logging
import discord
from discord.ext import commands


# logger stuff yeah
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER_HANDLER = logging.FileHandler(
    filename="logs/{}.log".format(__name__), encoding='utf-8', mode='w')
LOGGER_HANDLER.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(LOGGER_HANDLER)


class Announcment:
    """Announcment command."""

    def __init__(self, bot):
        self.bot = bot

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    @commands.command(hidden=True)
    async def announce(self, ctx, *, mess: str):
        if ctx.message.author.id == self.bot.owner_id:
            guilds = self.bot.guilds
            for guild in guilds:
                channel = guild.default_channel
                await channel.send(mess)


def setup(bot):
    bot.add_cog(Announcment(bot))
