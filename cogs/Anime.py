"""ok"""
import json
from textwrap import shorten
import time
import logging
import os

import requests

import discord
from discord.ext import commands

# pylint: disable=W1202
# pylint: disable=W0703

# logger stuff yeah
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER_HANDLER = logging.FileHandler(
    filename="logs/{}.log".format(__name__), encoding='utf-8', mode='w')
LOGGER_HANDLER.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(LOGGER_HANDLER)


class Anime:
    """weeb cog class"""

    def __init__(self, bot):
        self.bot = bot
        self.thingy = os.path.dirname('__file__')
        self.config = os.path.join(self.thingy, "../config/anime.json")
        self.url = "https://anilist.co/api/auth/access_token"
        self.token = ""
        self.refresh_time = 0

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    def create(self):
        """creates an access token"""
        if time.time() >= self.refresh_time:
            with open(self.config) as file:
                data = json.load(file)

            secret = data['secret']
            id_thing = data['id']

            creds = {
                "grant_type": "client_credentials",
                "client_id": id_thing,
                "client_secret": secret
            }

            r = requests.post(self.url,
                              json=creds)
            req = r.json()

            self.token = req["access_token"]
            self.refresh_time = req["expires"]


    @commands.command()
    async def character(self, ctx, *, character: str):
        """Shows info about an anime character."""
        self.create()

        character_url = "https://anilist.co/api/character/search/{}".format(
            character)
        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }
        req = requests.get(character_url, headers=headers)
        r = req.json()

        if r[0]["name_last"] is not None:
            charName = "{} {}".format(r[0]["name_first"], r[0]["name_last"])
        else:
            charName = r[0]["name_first"]

        niga = {
            "Name": charName,
            "**Info:**": r[0]["info"],
            "Image": r[0]["image_url_lge"]
        }

        niga["**Info:**"] = niga["**Info:**"].replace("<br>", "\n")
        niga["**Info:**"] = niga["**Info:**"].replace("&#039;", "'")
        niga["**Info:**"] = niga["**Info:**"].replace("&rsquo;", "'")
        niga["**Info:**"] = niga["**Info:**"].replace("~!", "**SPOILERS** ")
        niga["**Info:**"] = niga["**Info:**"].replace("!~", " **SPOILERS**")
        niga["**Info:**"] = niga["**Info:**"].replace("__", "**")

        if len(niga["**Info:**"]) >= 2048:
            niga["**Info:**"] = shorten(niga["**Info:**"],
                                        width=2045,
                                        placeholder="...")
            boolThing = True
        else:
            boolThing = False

        em = discord.Embed(title=niga["Name"],
                           description=niga["**Info:**"],
                           color=ctx.message.author.color)
        em.set_image(url=niga["Image"])

        if (boolThing == True):
            em.add_field(name="Info (Discord message limit was hit):",
                         value="https://anilist.co/character/{}".format(r[0]["id"]))
        await ctx.send(embed=em)

    @commands.command()
    async def anime(self, ctx, *, title: str):
        """Shows info about an anime."""
        self.create()
        title_url = "https://anilist.co/api/anime/search/{}".format(title)

        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }
        req = requests.get(title_url, headers=headers)
        r = req.json()

        niga = {
            "Title": r[0]["title_romaji"],
            "**Description:**": r[0]["description"],
            "**Type:**": r[0]["type"],
            "**Hentai?**": str(r[0]["adult"]),
            "**Average Score:**": "{}/100".format(str(r[0]["average_score"])),
            "**Popularity:**": str(r[0]["popularity"]),
            "**Total Episodes:**": str(r[0]["total_episodes"]),
            "**Episode Duration:**": "{} minutes".format(str(r[0]["duration"])),
            "**Status:**": r[0]["airing_status"].title() + ".",
            "Image": r[0]["image_url_lge"]
        }
        niga["**Description:**"] = niga["**Description:**"].replace(
            "<br>", "\n")
        niga["**Description:**"] = niga["**Description:**"].replace(
            "&rsquo;", "'")
        niga["**Description:**"] = niga["**Description:**"].replace(
            "~!", "**SPOILERS** ")
        niga["**Description:**"] = niga["**Description:**"].replace(
            "!~", " **SPOILERS**")
        niga["**Description:**"] = niga["**Description:**"].replace("__", "**")
        niga["**Description:**"] = niga["**Description:**"].replace(
            "&#039;", "'")
        if len(niga["**Description:**"]) >= 2048:
            niga["**Description:**"] = shorten(niga["**Description:**"],
                                               width=2045,
                                               placeholder="...")
            boolThing = True
        else:
            boolThing = False
        em = discord.Embed(title=niga["Title"],
                           color=ctx.message.author.color)
        for key in niga.keys():
            if key in ["Title", "Image"]:
                continue
            val = niga[key]
            em.add_field(name=key, value=val)
        em.set_image(url=niga["Image"])
        if boolThing:
            em.add_field(name="Description (Discord message limit was hit):",
                         value="https://anilist.co/anime/{}".format(r[0]["id"]))
        await ctx.send(embed=em)

    @commands.command()
    async def manga(self, ctx, *, title: str):
        """Shows info about a manga."""
        self.create()
        title_url = "https://anilist.co/api/manga/search/{}".format(title)
        headers = {
            "Authorization": "Bearer {}".format(self.token)
        }
        req = requests.get(title_url, headers=headers)
        r = req.json()
        niga = {
            "Title": r[0]["title_romaji"],
            "**Description:**": r[0]["description"],
            "**Type:**": r[0]["type"],
            "**Doujin?**": str(r[0]["adult"]),
            "**Mean Score:**": "{}/100".format(str(r[0]["mean_score"])),
            "**Popularity:**": str(r[0]["popularity"]),
            "**Total Chapters:**": str(r[0]["total_chapters"]),
            "**Total Volumes:**": str(r[0]["total_volumes"]),
            "**Status:**": r[0]["publishing_status"].title() + ".",
            "Image": r[0]["image_url_lge"]
        }
        niga["**Description:**"] = niga["**Description:**"].replace(
            "<br>", "\n")
        niga["**Description:**"] = niga["**Description:**"].replace(
            "&rsquo;", "'")
        niga["**Description:**"] = niga["**Description:**"].replace(
            "~!", "**SPOILERS** ")
        niga["**Description:**"] = niga["**Description:**"].replace(
            "!~", " **SPOILERS**")
        niga["**Description:**"] = niga["**Description:**"].replace("__", "**")
        niga["**Description:**"] = niga["**Description:**"].replace(
            "&#039;", "'")

        if len(niga["**Description:**"]) >= 2048:
            niga["**Description:**"] = shorten(niga["**Description:**"],
                                               width=2045,
                                               placeholder="...")
            boolThing = True
        else:
            boolThing = False

        em = discord.Embed(title=niga["Title"],
                           color=ctx.message.author.color)

        for key in niga.keys():
            if key in ["Title", "Image"]:
                continue
            val = niga[key]
            em.add_field(name=key, value=val)
        em.set_image(url=niga["Image"])
        if boolThing:
            em.add_field(name="Description (Discord message limit was hit):",
                         value="https://anilist.co/manga/{}".format(r[0]["id"]))
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Anime(bot))
