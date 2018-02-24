"""it exists"""
import logging
import random
import base64

import json

from urllib.request import urlopen
from discord.ext import commands

import discord

# pylint: disable=W1202

# logger stuff yeah
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER_HANDLER = logging.FileHandler(
    filename="logs/{}.log".format(__name__), encoding='utf-8', mode='w')
LOGGER_HANDLER.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(LOGGER_HANDLER)


class Fun:
    # pylint: disable=R0904
    # pylint: disable=C0330

    def __init__(self, bot):
        self.bot = bot

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    @commands.command()
    async def emojify(self, ctx, *, mess):
        """emojifies a message"""
        # shamelessly (kind of) stolen from lunar and supersebi3
        message = ""
        for exa in mess:
            if exa in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ":
                if exa != " ":
                    message = "{}{}".format(message, exa.replace(
                        exa, ":regional_indicator_{}:".format(exa).lower()))
                elif exa == " ":
                    message = message + "    "
        await ctx.send(message)

    @commands.command()
    async def decode(self, ctx, base: str, *, msg: str):
        """decodes stuff in base64, base32, etc..."""
        if base == "base64":
            exa = base64.b64decode(msg.encode('utf-8'))
            await ctx.send(exa.decode())
        if base == "base16":
            exa = base64.b16decode(msg.encode('utf-8'))
            await ctx.send(exa.decode())
        if base == "base32":
            exa = base64.b32decode(msg.encode('utf-8'))
            await ctx.send(exa.decode())
        if base == "base85":
            exa = base64.b85decode(msg.encode('utf-8'))
            await ctx.send(exa.decode())

    @commands.command()
    async def encode(self, ctx, base: str, *, msg: str):
        """encodes stuff in base64, base32, etc..."""
        if base == "base64":
            exa = base64.b64encode(msg.encode('utf-8'))
            await ctx.send(exa.decode())
        if base == "base16":
            exa = base64.b16encode(msg.encode('utf-8'))
            await ctx.send(exa.decode())
        if base == "base32":
            exa = base64.b32encode(msg.encode('utf-8'))
            await ctx.send(exa.decode())
        if base == "base85":
            exa = base64.b85encode(msg.encode('utf-8'))
            await ctx.send(exa.decode())

    @commands.command()
    @commands.cooldown(rate=2, per=2, type=commands.BucketType.user)
    async def cat(self, ctx):
        """sends an image from random.cat"""
        url = "http://random.cat/meow"

        with urlopen(url) as url:
            data = json.loads(url.read().decode())

        msg = discord.Embed(title="random.cat image",
                            color=ctx.message.author.color)
        msg.set_image(url=data["file"])

        await ctx.send(embed=msg)

    @commands.command()
    async def bify(self, ctx, *, msg: str):
        """replaces all B-s in a message with red B emojis"""
        msg = msg.replace("b", ":b:")
        msg = msg.replace("B", ":b:")
        await ctx.send(msg)

    @commands.command()
    async def vaporwaveify(self, ctx, *, msg: str):
        """makes a message 'aesthetic'"""
        await ctx.send(msg.replace("", " ")[1: -1].upper())

    @commands.command(name='8ball')
    async def _8ball(self, ctx):
        """asks the 8ball something"""
        answers = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes, definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "The outlook is good.",
            "Yes.",
            "Signs point to yes",
            "Reply is hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict right now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "The outlook is not so good.",
            "Very doubtful."
        ]

        await ctx.send(random.choice(answers))

    @commands.command()
    async def random_user(self, ctx):
        """mention a random user from the server."""
        members = ctx.message.guild.members
        member = random.choice(members).mention

        # i probably shouldn't do this
        while member == self.bot.user.mention:
            member = random.choice(members)

        await ctx.send("{}!".format(member))


def setup(bot):
    bot.add_cog(Fun(bot))
