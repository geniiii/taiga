"""woah!!!"""
# BROKEN - Don't use.
import sys
import asyncio
import os
import logging
from ctypes.util import find_library
import discord
from discord.ext import commands
import discord.voice_client
import youtube_dl

# pylint: disable=W1202

#logger stuff yeah
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
LOGGER_HANDLER = logging.FileHandler(filename=__name__ + ".log", encoding='utf-8', mode='w')
LOGGER_HANDLER.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
LOGGER.addHandler(LOGGER_HANDLER)

class LogThing(object):
    """logger for yt_dl"""
    @staticmethod
    def debug(msg):
        """woops it died"""
        LOGGER.debug(msg)
    @staticmethod
    def warning(msg):
        """woops it died"""
        LOGGER.warning(msg)
    @staticmethod
    def error(msg):
        """woops it died"""
        LOGGER.error(msg)

def ayylmao(data):
    """the progress hook"""
    if data['status'] == 'finished':
        LOGGER.info("Done downloading, now converting...")


class Experimental:
    """music commands!!!"""
    def __init__(self, bot):
        self.bot = bot
        self.thingy = os.path.dirname('__file__')
        self.config = os.path.join(self.thingy, "config/config.json")

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    ydl_opts = {

        'format': 'bestaudio/best',
        'outtmpl': 'music/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'LOGGER': LogThing(),
        'progress_hooks': [ayylmao],
    }
    @commands.command()
    async def playyt(self, ctx, *, url: str):
        """Plays music from Youtube."""
        if os.system is "nt":
            opus_path = os.path.join(self.thingy, "libs/libopus.dll")
            discord.opus.load_opus(opus_path)
        elif os.system is "posix" and sys.platform is not "Darwin":
            opus_path = find_library("opus")
            if opus_path is None:
                print("Looks like I failed to find the library.")
                print("If you're on BSD or Linux, make sure you have Opus installed.")
            else:
                discord.opus.load_opus(opus_path)
        elif sys.platform is "Darwin":
            print("Darwin/macOS is not supported yet.")
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
        else:
            ctx.send("join a voice channel first you cunt")
        guild = ctx.message.guild
        if guild.voice_client is not None:
            nagisa_vc = guild.voice_client
            if nagisa_vc.is_playing:
                nagisa_vc.stop()
        else:
            nagisa_vc = await channel.connect()
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
        if video_title is not None:
            video_title = video_title.replace("|", "_")
            video_title = video_title.replace("/", "_")
            video_title = video_title.replace('"', "'")
        source = discord.FFmpegPCMAudio("music/" + str(video_title) + ".mp3")
        source = discord.PCMVolumeTransformer(source)
        nagisa_vc.play(source, after=lambda: auto_disconnect(vc=nagisa_vc))

    @commands.command(pass_context=True)
    async def stop(self, ctx):
        """Disconnects from the voice channel."""


    #@commands.command()
    #async def clean(self):
        # Don't use.
        #shutil.rmtree('D:/nagisa/music')
        #os.mkdir("D:/nagisa/music")

    @commands.command(pass_context=True)
    async def volume(self, ctx, volume: float):
        """Changes the music's volume."""
        guild = ctx.message.guild
        nagisa_vc = guild.voice_client
        nagisa_vc.source.volume = volume

    @commands.command(pass_context=True)
    async def pause(self, ctx):
        """Pauses the music."""
        guild = ctx.message.guild
        nagisa_vc = guild.voice_client
        await nagisa_vc.pause()

    @commands.command(pass_context=True)
    async def unpause(self, ctx):
        """Unpauses the music."""
        guild = ctx.message.guild
        nagisa_vc = guild.voice_client
        await nagisa_vc.unpause()


def setup(bot):
    """adds the cog as a cog"""
    bot.add_cog(Experimental(bot))
