"""ok"""
from __main__ import start_time

import json
import logging
import os
import datetime
import psutil


from urllib import request
from urllib.request import urlopen

import discord
from discord.ext import commands
import requests

# pylint: disable=W1202
# pylint: disable=W0703

# logger stuff yeah
LOGGER_PATH = os.path.dirname('__file__')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER_HANDLER = logging.FileHandler(
    filename="logs/{}.log".format(__name__), encoding='utf-8', mode='w')
LOGGER_HANDLER.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(LOGGER_HANDLER)


class Info:
    """info cog class"""

    def __init__(self, bot):
        self.bot = bot

        thingy = os.path.dirname(os.path.abspath(__file__))
        self.config = os.path.join(thingy, "../config/config.json")
        self.nagisa = os.path.join(thingy, "../config/taiga.json")
        self.osu_config = os.path.join(thingy, "../config/osu.json")

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member):  # hacky mess
        """Shows info about a user."""
        created_at = user.created_at.replace(microsecond=0)
        joined_at = user.joined_at.replace(microsecond=0)

        roles = "`"

        for role in user.roles:
            roles += "{}, ".format(role.name)
        roles = roles[:-2]
        roles += '`'

        info = {"Name:": user.name,
                "Avatar:": user.avatar_url,
                "ID:": user.id,
                "Bot:": str(user.bot),
                "Created at:": created_at,
                "Joined at:": joined_at,
                "Game:": str(user.game),
                "Nickname": str(user.nick),
                "Highest role:": str(user.top_role),
                "Roles:": roles}

        embed = discord.Embed(title=info["Name:"], colour=user.colour)
        embed.set_image(url=info["Avatar:"])

        for key in info:
            if key in ["Name:", "Avatar:"]:
                continue

            val = info[key]
            embed.add_field(name=key, value=val)

        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        """Shows info about the server."""
        guild = ctx.message.guild
        created_at = guild.created_at.replace(microsecond=0)

        info = {
            "Created at:": created_at,
            "Name:": str(guild.name),
            "Owner:": str(ctx.message.guild.owner),
            "Verification Level:": str(guild.verification_level),
            "Icon:": str(guild.icon_url),
            "Role count:": len(guild.roles),
            "Custom emoji count:": len(guild.emojis),
            "Channel count:": len(guild.channels),
            "Region:": str(guild.region),
            "Member count:": guild.member_count,
            "ID:": str(guild.id)
        }

        embed = discord.Embed(
            title=info["Name:"], colour=ctx.message.guild.owner.colour)
        embed.set_thumbnail(url=info["Icon:"])
        for key in info:
            if key in ["Name:", "Icon:"]:
                continue
            val = info[key]
            embed.add_field(name=key, value=val)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(rate=3, per=5, type=commands.BucketType.user)
    async def owinfo(self, ctx, user_id: str, region: str):
        """Shows info about an Overwatch player."""
        user_id = user_id.replace("#", "-")
        region = region.lower()
        url = "http://owapi.net/api/v3/u/{}/blob".format(user_id)

        LOGGER.info("ow api url: %s", url)

        req = request.Request(
            url, headers={'User-Agent': "xxl sakujes browser"})

        data = requests.get(url).json

        info = {
            "Name:": user_id.replace("-", "#"),
            "Avatar:": data[region]["stats"]["quickplay"]["overall_stats"][str("avatar")],
            "**Region: **": region.upper(),
            "**Level: **": data[region]["stats"]["quickplay"]["overall_stats"][str("level")],
            "**Rank: **": data[region]["stats"]["quickplay"]["overall_stats"]["tier"],
            "**Quick Play Wins: **": data[region]["stats"]["quickplay"]
            ["overall_stats"][str("wins")],
            "**Quick Play Losses: **": data[region]["stats"]["quickplay"]
            ["overall_stats"][str("losses")],
            "**Quick Play Eliminations: **": data[region]["stats"]["quickplay"]
            ["game_stats"][str("eliminations")],
            "**Quick Play Deaths: **": data[region]["stats"]["quickplay"]
            ["game_stats"][str("deaths")],
            "**Quick Play KDR: **": str(data[region]["stats"]["quickplay"]["game_stats"]
                                        ["eliminations"] /
                                        data[region]["stats"]
                                        ["quickplay"]["game_stats"]["deaths"]),
        }

        if data[region]["stats"]["competitive"] is not None:
            user_id_comp = {
                "**Competitive Eliminations: **": data[region]["stats"]
                ["competitive"]["game_stats"]
                [str("eliminations")],
                "**Competitive Deaths: **": data[region]["stats"]
                ["competitive"]["game_stats"][str("deaths")],
                "**Competitive Wins: ** ": data[region]["stats"]
                ["competitive"]["overall_stats"][str("wins")],
                "**Competitive Losses: ** ": data[region]["stats"]
                ["competitive"]["overall_stats"][str("losses")],
                "**Competitive KDR: **": str(data[region]["stats"]
                                             ["competitive"]["game_stats"]["eliminations"] /
                                             data[region]["stats"]["competitive"]
                                             ["game_stats"]["deaths"]),
            }
            xxl = {**info, **user_id_comp}
        else:
            xxl = info
        try:
            xxl["**Rank: **"] = xxl["**Rank: **"].title()
        except Exception:
            xxl["**Rank: **"] = "None"

        embed = discord.Embed(
            title=xxl["Name:"], colour=ctx.message.author.colour)
        embed.set_image(url=xxl["Avatar:"])
        link = ""

        if xxl["**Rank: **"] == "Bronze":
            link = "http://i.imgur.com/tHld9yz.png"
        elif xxl["**Rank: **"] == "Silver":
            link = "http://i.imgur.com/IOt3CTv.png"
        elif xxl["**Rank: **"] == "Gold":
            link = "http://i.imgur.com/Q9wGr6d.png"
        elif xxl["**Rank: **"] == "Platinum":
            link = "http://i.imgur.com/RrPCNM1.png"
        elif xxl["**Rank: **"] == "Diamond":
            link = "http://i.imgur.com/fkw2cxN.png"
        elif xxl["**Rank: **"] == "Master":
            link = "http://i.imgur.com/HPbH7uV.png"
        elif xxl["**Rank: **"] == "Grandmaster":
            link = "http://i.imgur.com/xdPsP4w.png"

        embed.set_thumbnail(url=link)

        for key in xxl.keys():
            if key in ["Name:", "Avatar:"]:
                continue
            val = xxl[key]
            embed.add_field(name=key, value=val)

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Sends an invite URL for the bot."""
        thingy = os.path.dirname(os.path.abspath(__file__))
        config = os.path.join(thingy, "config/config.json")

        with open(config) as file:
            data = json.load(file)
        invite = data['invite']

        await ctx.send("Invite URL: {}".format(invite))

    @commands.command()
    async def osu(self, ctx, *, user: str):
        """Shows info about an osu! player."""
        url = "https://osu.ppy.sh/api/get_user?k={}&u={}"
        thingy = os.path.dirname(os.path.abspath(__file__))
        countries = os.path.join(thingy, "../osu/countries.json")
        with open(self.osu_config) as file:
            data = json.load(file)
        key = data['key']

        url = url.format(key, user)
        r = requests.get(url).json()

        info = {
            "user_id": r[0]["user_id"],
            "name": r[0]["username"],
            "country": r[0]["country"],
            "**Total attempts: **": r[0]["playcount"],
            "**Level: **": r[0]["level"],
            "**PP: **": r[0]["pp_raw"],
            "**Accuracy: **": r[0]["accuracy"] + '%'
        }

        with open(countries) as file:
            clist = json.load(file)
            country = clist[info["country"]]

        color = discord.Colour.from_rgb(255, 109, 238)

        em = discord.Embed(title=info["name"],
                           colour=color)

        for key in info.keys():
            if key in ["user_id", "name", "country"]:
                continue
            val = info[key]
            em.add_field(name=key, value=val)

        em.add_field(name="**Country: **", value=country)
        em.set_image(url="https://a.ppy.sh/{}".format(info["user_id"]))
        await ctx.send(embed=em)

    @commands.command()
    async def poll(self, ctx, *, question: str):
        """Makes a poll about something."""
        poll_em = discord.Embed(title="Poll",
                                description=question,
                                color=discord.Color.green())

        msg = await ctx.send(embed=poll_em)

        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

    @commands.command(name='bot')
    async def __bot(self, ctx):
        """Sends info about the bot."""
        with open(self.config) as file:
            config = json.load(file)
        version = config["version"]

        em = discord.Embed(title=self.bot.user.name,
                           color=discord.Color.green())

        bot_info = self.bot.application_info()
        process = psutil.Process(os.getpid())

        now = datetime.datetime.now().replace(microsecond=0)
        uptime = now - start_time.replace(microsecond=0)

        # the bot's name
        em.add_field(name="**Name: **", value=self.bot.user.name)
        # the bot's description
        em.add_field(name="**Description: **", value=self.bot.description)
        # the bot's uptime
        em.add_field(name="**Uptime: **", value=str(uptime))
        # the bot's invite url
        em.add_field(name="**Invite URL: **",
                     value="https://discordapp.com/api/oauth2/authorize?client_id={}&permissions=8&scope=bot".format(str(self.bot.user.id)))
        # amount of custom emojis the bot can use
        em.add_field(name="**Total Custom Emojis: **",
                     value=len(self.bot.emojis))
        # amount of guilds the bot is in
        em.add_field(name="**Total Guilds: **", value=len(self.bot.guilds))
        em.add_field(name="**CPU Usage: **",
                     value=str(process.cpu_percent()) + "%")
        em.add_field(name="**RAM Usage: **",
                     value=str(process.memory_info().rss / float(2 ** 20)) + "MB")
        em.add_field(name="**Bot Version: **", value=version)
        em.add_field(name="**discord.py Version: **",
                     value=str(discord.__version__))
        em.add_field(name="**ID: **", value=str(self.bot.id))
        em.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=em)


def setup(bot):
    """ok"""
    bot.add_cog(Info(bot))
