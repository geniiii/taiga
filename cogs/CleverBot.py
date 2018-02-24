"""ok"""
import json
import logging
import os
import requests

import discord
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

thingy = os.path.dirname(os.path.abspath(__file__))
config = os.path.join(thingy, "../config/cleverbot.json")

with open(config) as file:
    data = json.load(file)
    user = data["api_user"]
    key = data["api_key"]


class CleverBot:
    def __init__(self, bot):
        self.bot = bot
        self.people = []

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    @commands.command()
    async def clever(self, ctx, *, msg: str):
        cred = {
            'user': user,
            'key': key,
            'nick': ctx.message.author.display_name,
            'text': msg
        }

        cred2 = {
            'user': user,
            'key': key,
            'nick': ctx.message.author.display_name,
        }

        if cred['nick'] not in self.people:
            self.people.append(cred['nick'])
            requests.post("https://cleverbot.io/1.0/create", json=cred2)

        req = requests.post("https://cleverbot.io/1.0/ask", json=cred)
        r = json.loads(req.text)

        if r['status'] == 'success':
            message = r['response']
            await ctx.send(message)
        else:
            await ctx.send("An error has occured.")
            print(cred['nick'])
            print(r['status'])


def setup(bot):
    bot.add_cog(CleverBot(bot))
