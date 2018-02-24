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
    """owner commands!!!"""

    def __init__(self, bot):
        self.bot = bot

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    @commands.is_owner()
    @commands.command()
    async def say(self, ctx, *, mess: str):
        """says stuff in the chat"""
        await ctx.send(mess)

    @commands.is_owner()
    @commands.command()
    async def saytts(self, ctx, *, mess: str):
        """Says stuff in the chat. (TTS)"""
        await ctx.send(mess,
                       tts=True)


def setup(bot):
    """woaah!!!"""
    bot.add_cog(Owner(bot))
