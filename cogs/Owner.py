"""ok"""
import logging
from discord.ext import commands

# pylint: disable=W1202

# logger stuff yeah
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER_HANDLER = logging.FileHandler(
    filename="logs/{}.log".format(__name__), encoding='utf-8', mode='w')
LOGGER_HANDLER.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(LOGGER_HANDLER)


class Owner:
    """owner command!!!"""

    def __init__(self, bot):
        self.bot = bot

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    @commands.command(pass_context=True)
    async def say(self, ctx, *, mess: str):
        """Says stuff in the chat."""
        if ctx.message.author.id == self.bot.owner_id:
            await ctx.send(mess)
        else:
            await ctx.send("You aren't the bot owner.")

    @commands.command(pass_context=True)
    async def saytts(self, ctx, *, mess: str):
        """Says stuff in the chat. (TTS)"""
        if ctx.message.author.id == self.bot.owner_id:
            await ctx.send(mess, tts=True)
        else:
            await ctx.send("You aren't the bot owner.")


def setup(bot):
    """woaah!!!"""
    bot.add_cog(Owner(bot))
