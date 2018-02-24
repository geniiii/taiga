import discord
import datetime

async def mod(channel_name, guild, user, title, message, color, timestamp_msg):
    timestamp = datetime.datetime.now()
    timestamp.strftime('%H:%M:%S, %d (%A) %B %Y')
    timestamp = timestamp.replace(microsecond=0)

    channel = discord.utils.get(guild.text_channels, name=channel_name)

    em = discord.Embed(title=title, description=message, color=color)
    em.set_footer(text="{} Notification | {}".format(timestamp_msg, timestamp),
                  icon_url=user.avatar_url)

    await channel.send(embed=em)

async def mod_lockdown(channel_name, guild, title, message, color, timestamp_msg):
    timestamp = datetime.datetime.now()
    timestamp.strftime('%H:%M:%S, %d (%A) %B %Y')
    timestamp = timestamp.replace(microsecond=0)

    channel = discord.utils.get(guild.text_channels, name=channel_name)

    em = discord.Embed(title=title, description=message, color=color)
    em.set_footer(text="{} Notification | {}".format(timestamp_msg, timestamp))

    await channel.send(embed=em)

