"""exa"""
import logging
from urllib.parse import quote_plus
import discord

from discord.ext import commands

import aiohttp

# pylint: disable=W0702
# pylint: disable=W1202

#logger stuff yeah
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER_HANDLER = logging.FileHandler(filename="logs/{}.log".format(__name__), encoding='utf-8', mode='w')
LOGGER_HANDLER.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(LOGGER_HANDLER)

class UrbanDictionary:
    """exa"""
    def __init__(self, bot):
        self.bot = bot

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    @commands.command()
    async def urban(self, ctx, *, search_terms: str):
        """Searches for something on urban dictionary."""
        def encode(exa):
            """exa"""
            return quote_plus(exa, encoding='utf-8', errors='replace')
        search_terms = search_terms.split(" ")
        try:
            if len(search_terms) > 1:
                pos = int(search_terms[-1]) - 1
                search_terms = search_terms[:-1]
            else:
                pos = 0
            if pos not in range(0, 11):  # API only provides the
                pos = 0  # top 10 definitions
        except ValueError:
            pos = 0

        search_terms = "+".join([encode(s) for s in search_terms])
        url = "http://api.urbandictionary.com/v0/define?term=" + search_terms
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as rexa:
                    result = await rexa.json()
            if result["list"]:
                definition = result['list'][pos]['definition']
                example = result['list'][pos]['example']
                defs = len(result['list'])
                clannad = "**Definition #{} out of {}:\n**{}\n\n""**Example:\n**{}"
                msg = (discord.Embed(description=
                                     clannad.format(pos + 1,
                                                    defs, definition, example) +
                                     "**\n\nThumbs up:\n**" + str(result['list']
                                                                  [pos]['thumbs_up']) +
                                     "**\n\nThumbs down:\n**" + str(result['list']
                                                                    [pos]['thumbs_down']),
                                     title=result['list'][pos]['word'],
                                     colour=discord.Colour.green()))
                await ctx.send(embed=msg)
            else:
                await ctx.send("No results found.")
        except IndexError:
            await ctx.send("No definition for #{}.".format(pos + 1))
        except:
            await ctx.send("woops i died")


def setup(bot):
    """exa"""
    bot.add_cog(UrbanDictionary(bot))
