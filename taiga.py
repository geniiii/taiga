import json

import os
import logging
import datetime

import discord
from discord import Forbidden, ConnectionClosed
from discord.ext import commands
from discord.opus import OpusError, OpusNotLoaded
from discord.ext.commands import CommandOnCooldown, CommandNotFound, NotOwner

# pylint: disable=W0703
# pylint: disable=W1202

start_time = datetime.datetime.now()


def taiga():  # the bot's function
    """the main thing"""
    # config stuff
    cogs_json = "config/cogs.json"  # cog list
    config = "config/config.json"  # config file

    with open(config) as file:
        data = json.load(file)
    prefix = data['prefix']
    description = data['description']
    token = data['token']
    # making sure it's an int even if someone makes it a string
    owner = int(data['owner_id'])

    version = data['version']
    log_name = data['log']
    pm_help = data['pm_help']

    # logging shit
    taiga_log = logging.getLogger("discord")
    taiga_log.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename="logs/{}".format(log_name), encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    taiga_log.addHandler(handler)

    # the bot
    bot = commands.Bot(
        command_prefix=prefix,
        description=description,
        owner_id=owner)

    if pm_help.lower() == 'true':  # pm help checks
        bot.pm_help = True

    @bot.async_event
    async def on_ready():
        """does stuff when the bot is ready"""  # pretty much
        servers = len(bot.guilds)
        game = discord.Game(name=data['game'].format(
            bot.command_prefix, str(servers)))
        await bot.change_presence(game=game)  # changes the game
        print("Username: {}".format(bot.user.name))
        print("ID: {}".format(str(bot.user.id)))
        print("Prefix: {}".format(bot.command_prefix))
        print("Version: {}".format(version))
        print("Game: {}".format(game))
        print("Description: {}".format(description))
        print("Owner ID: {}".format(str(owner)))

    async def prlog(msg, etype):
        print(msg)
        if etype == "error":
            taiga_log.error(msg)
        elif etype == "warning":
            taiga_log.warning(msg)
        elif etype == "info":
            taiga_log.info(msg)

    @bot.async_event
    async def on_command_error(ctx, error):
        channel = ctx.message.channel
        if isinstance(error, CommandOnCooldown):
            await channel.send("the command {.command} is on cooldown, {}. wait {:.2f} seconds to use it again.".format(ctx,
                                                                                                                        ctx.message.author.name,
                                                                                                                        error.retry_after))
        elif isinstance(error, CommandNotFound):
            await channel.send("command not found.")
        elif isinstance(error, NotOwner):
            await channel.send("hey! you're not the bot's owner.")
        elif isinstance(error, OpusError):
            await prlog("libopus error: {}".format(error), "error")
        elif isinstance(error, OpusNotLoaded):
            await prlog("libopus isn't loaded: {}".format(error), "error")
        elif isinstance(error, ConnectionClosed):
            await prlog("connection closed? possibly internet connection issue. reason: {}\ncode: {}\n shard ID: {}".format(error.reason, error.code, error.shard_id), "error")
        elif isinstance(error, Forbidden):
            await channel.send("i have no permissions to do that")

    with open(cogs_json) as cogs_list:
        cogs = json.load(cogs_list)

    for value in cogs:
        try:
            bot.load_extension(value)  # tries to load extensions
            msg = "Loaded extension {}.".format(value)
            print(msg)
            taiga_log.info(msg)
        except ImportError as thing:
            exc = "{}: {}".format(
                type(thing).__name__, thing)  # the exception
            msg = "Failed to load extension {}\n{}".format(value, exc)
            print(msg)
            taiga_log.error(msg)
        except discord.ClientException as thing:
            msg = "{} doesn't have a setup function.".format(value)
            print(msg)
            taiga_log.error(msg)
        except Exception as thing:
            exc = "{}: {}".format(
                type(thing).__name__, thing)
            msg = "Failed to load extension {}\n{}".format(value, exc)
            print(msg)
            taiga_log.error(msg)

    # debug commands
    @bot.command(hidden=True)
    @commands.is_owner()
    async def load_cog(ctx, *, cog: str):  # loads a cog
        """Loads a cog."""
        try:
            bot.load_extension(cog)
        except Exception as thing:
            exc = "{}: {}".format(type(thing).__name__, thing)
            msg = "```Failed to load extension {}\n{}```".format(cog, exc)
            await ctx.send(msg)

    @bot.command(hidden=True)  # unloads a cog
    @commands.is_owner()
    async def unload_cog(ctx, *, cog: str):
        """Unloads a cog."""
        try:
            bot.unload_extension(cog)
        except Exception as thing:
            exc = "{}: {}".format(type(thing).__name__, thing)
            msg = "```Failed to unload extension {}\n{}```".format(cog, exc)
            await ctx.send(msg)

    @bot.command(hidden=True)  # reloads a cog
    @commands.is_owner()
    async def reload_cog(ctx, *, cog: str):
        """Reloads a cog."""
        try:
            bot.unload_extension(cog)
            bot.load_extension(cog)
        except Exception as thing:
            exc = "{}: {}".format(type(thing).__name__, thing)
            msg = "```Failed to reload extension {}\n{}```".format(cog, exc)
            await ctx.send(msg)

    bot.run(token)


if __name__ == "__main__":
    taiga()  # runs the bot
