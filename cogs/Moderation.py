"""moderation commands!!!"""
import logging
import discord
import json
import os
from asyncio import TimeoutError, sleep
from discord.ext import commands
from cogs.utils import mod_utils

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
config = os.path.join(thingy, "../config/logging.json")
other_config = os.path.join(thingy, "../config/auto_roles.json")


class Moderation:
    """moderation commands, require permissions"""

    def __init__(self, bot):
        self.bot = bot
        with open(config, encoding='utf8') as file:
            data = json.load(file)
        # channel stuff
        self.mod_channel_name = data["mod_channel"]
        # kick stuff
        self.kick_title = data["kick_title"]
        self.kick_msg = data["kick_msg"]
        # ban stuff
        self.ban_title = data["ban_title_cmd"]
        self.ban_msg = data["ban_msg_cmd"]
        # purge stuff
        self.purge_title = data["purge_title"]
        self.purge_msg = data["purge_msg"]
        # lockdown stuff
        self.lockdown_role = data["lockdown_role"]
        self.lockdown_title = data["lockdown_title"]
        self.lockdown_msg = data["lockdown_msg"]
        self.unlockdown_title = data["unlockdown_title"]
        self.unlockdown_msg = data["unlockdown_msg"]
        self.lockdown = []
        # timeout stuff
        self.timeout_role = data["timeout_role"]
        self.timeout_title = data["timeout_title"]
        self.timeout_msg = data["timeout_msg"]
        self.untimeout_title = data["untimeout_title"]
        self.untimeout_msg = data["untimeout_msg"]
        # lockdown and timeout role stuff (does this even work!?)
        self.timeout_ow = discord.PermissionOverwrite()
        self.timeout_ow.update(send_messages=False, add_reactions=False)
        self.timeout_ow_vc = discord.PermissionOverwrite()
        self.timeout_ow_vc.update(connect=False, speak=False)

    async def on_member_join(self, member):
        if member.guild.id in self.lockdown:
            role = discord.utils.get(
                member.guild.roles, name=self.lockdown_role)
            await member.add_roles(role)

    async def __after_invoke(self, ctx):
        LOGGER.info('{0.command} is done...'.format(ctx))

    async def every_member_add(self, g, r):
        for member in g.members:
            await member.add_roles(r)

    async def every_member_remove(self, g, r):
        for member in g.members:
            await member.remove_roles(r)

    async def change_perms_text(self, guild, role, ow):
        for ch in guild.text_channels:
            try:
                await ch.set_permissions(role, overwrite=ow)
            except:
                pass

    async def change_perms_voice(self, guild, role, ow):
        for ch in guild.voice_channels:
            try:
                await ch.set_permissions(role, overwrite=ow)
            except:
                pass

    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        """Kicks people."""
        if ctx.message.author.guild_permissions.kick_members:
            try:
                await ctx.message.guild.kick(member)
                await ctx.send("Done.")
                await mod_utils.mod(self.mod_channel_name, ctx.message.guild, member,
                                    self.kick_title.format(member.name),
                                    self.kick_msg.format(
                                        member.name, ctx.message.author.name),
                                    discord.Colour.green(), "Kick")
            except discord.Forbidden:
                await ctx.send("I don't have permission to kick any members.")

        else:
            await ctx.send("You don't have permission to kick any members.")

    @commands.command()
    async def ban(self, ctx, member: discord.Member):
        """Bans people."""
        if ctx.message.author.guild_permissions.ban_members:
            try:
                await ctx.message.guild.ban(member)
                await ctx.send("Done.")
                await mod_utils.mod(self.mod_channel_name, ctx.message.guild, member,
                                    self.ban_title.format(member.name),
                                    self.ban_msg.format(
                                        member.name, ctx.message.author.name),
                                    discord.Colour.green(), "Ban")
            except discord.Forbidden:
                await ctx.send("I don't have permission to kick any members.")
        else:
            await ctx.send("You don't have permission to kick any members.")

    @commands.command()
    async def purge(self, ctx, member: discord.Member, mess_number: int):
        """Removes messages sent by a user."""
        def is_member(mess):
            """bad docstring"""
            return mess.author == member
        if ctx.message.author.guild_permissions.manage_messages is True:
            try:
                deleted = await ctx.message.channel.purge(limit=mess_number, check=is_member)
                await ctx.send('Deleted {} message(s) from this channel.'.format(len(deleted)))
                await mod_utils.mod(self.mod_channel_name, ctx.message.guild, member,
                                    self.purge_title,
                                    self.purge_msg.format(len(deleted),
                                                          member.name,
                                                          ctx.message.author.name),
                                    discord.Colour.green(),
                                    "Purge")
            except discord.Forbidden:
                await ctx.send("I have no permission to remove any messages. (Manage messages)")
        else:
            await ctx.send("You have no permissions to remove any messages. (Manage messages)")

    @commands.command()
    async def addrole(self, ctx, member: discord.Member, role: str):
        """Add a role to a user."""
        role = discord.utils.find(lambda m: m.name == role, ctx.guild.roles)
        if ctx.message.author.guild_permissions.manage_roles:
            if role is None:
                await ctx.send('The role "**{}**" does not exist.'.format(role))
            else:
                try:
                    await member.add_roles(role,
                                           reason="Command invoked by {}.".format(ctx.message.author.name))
                    await ctx.send('Successfully added role "**{}**" to user **{}**.'.format(role, member))
                except discord.Forbidden:
                    await ctx.send('I have no permission to add role "**{}**" to user **{}**. (Manage roles)'.format(role, member))
        else:
            await ctx.send("You have no permission to remove any roles. (Manage roles)")

    @commands.command()
    async def removerole(self, ctx, member: discord.Member, role: str):
        """Remove a role from a user."""
        role = discord.utils.find(lambda m: m.name == role, ctx.guild.roles)
        if ctx.message.author.guild_permissions.manage_roles:
            if role is None:
                await ctx.send('The role "**{}**" does not exist.'.format(role))
            else:
                try:
                    await member.remove_roles(role,
                                              reason="Command invoked by {}.".format(ctx.message.author.name))
                except discord.Forbidden:
                    await ctx.send('I have no permission to remove role "**{}**"" from user **{}**. (Manage roles)'.format(role, member))
        else:
            await ctx.send("You have no permission to remove any roles from any user. (Manage roles)")

    @commands.command(name='lockdown')
    async def __lockdown(self, ctx):
        """Put the server in a lockdown state."""
        if ctx.message.author.guild_permissions.manage_roles and ctx.message.author.guild_permissions.manage_channels:
            async def msg_thing():
                await mod_utils.mod_lockdown(self.mod_channel_name, ctx.message.guild,
                                             self.lockdown_title,
                                             self.lockdown_msg.format(
                                                 ctx.message.author.name),
                                             discord.Colour.red(),
                                             "Lockdown")
            msg = "Are you sure you want to put this server in lockdown mode?"
            msg2 = "Say 'lockdown yes' if you are 100% sure you want to. You have 30 seconds to respond."
            await ctx.send(msg)
            await ctx.send(msg2)
            user = ctx.message.author
            guild = ctx.message.guild
            lock_msg = "This server is currently in lockdown mode."

            def checkyes(m):
                return m.content == 'lockdown yes' and m.author == user
            try:
                m = await self.bot.wait_for('message', check=checkyes, timeout=30.0)
            except TimeoutError:
                await ctx.send("30 seconds have passed.")
            role = discord.utils.find(
                lambda m: m.name == self.lockdown_role, guild.roles)
            if role is None and m is not None:
                try:
                    await guild.create_role(name=self.lockdown_role,
                                            colour=discord.Colour.red(),
                                            permissions=discord.Permissions(permissions=66560))
                    role = discord.utils.find(
                        lambda m: m.name == self.lockdown_role, guild.roles)
                    try:
                        await self.every_member_add(g=guild, r=role)
                    except discord.Forbidden:
                        pass
                    await ctx.send(lock_msg)
                    await msg_thing()
                    self.lockdown.append(ctx.message.guild.id)
                    await self.change_perms_text(guild, role, self.timeout_ow)
                    await self.change_perms_voice(guild, role, self.timeout_ow_vc)
                except discord.Forbidden:
                    pass
            elif m is not None:
                try:
                    await self.every_member_add(g=guild, r=role)
                except discord.Forbidden:
                    pass
                await ctx.send(lock_msg)
                await msg_thing()
                self.lockdown.append(ctx.message.guild.id)
                await self.change_perms_text(guild, role, self.timeout_ow)
                await self.change_perms_voice(guild, role, self.timeout_ow_vc)
        else:
            await ctx.send("You have no permission to put the server on lockdown. (Manage Roles, Manage Channels)")

    @commands.command()
    async def unlockdown(self, ctx):
        """Puts the server outside of the lockdown state."""
        if ctx.message.author.guild_permissions.manage_roles and ctx.message.author.guild_permissions.manage_channels:
            role = discord.utils.find(
                lambda m: m.name == self.lockdown_role, ctx.message.guild.roles)
            if ctx.message.guild.id not in self.lockdown:
                await ctx.send("The server has not been in a lockdown state.")
            else:
                await self.every_member_remove(g=ctx.message.guild, r=role)
                await mod_utils.mod_lockdown(self.mod_channel_name, ctx.message.guild,
                                             self.unlockdown_title,
                                             self.unlockdown_msg.format(
                                                 ctx.message.author.name),
                                             discord.Colour.red(),
                                             "Unlockdown")
                self.lockdown.pop(ctx.message.guild.id)
        else:
            await ctx.send("You have no permission to put this server out of lockdown. (Manage Roles, Manage Channels)")

    @commands.command()
    async def timeout(self, ctx, member: discord.Member, seconds: int):
        """Timeouts a user for X amount of seconds."""
        if ctx.message.author.guild_permissions.manage_roles is False:
            await ctx.send("You have no permission to timeout members. (Manage Roles)")
            return

        async def msg_thing():
            await mod_utils.mod(self.mod_channel_name, ctx.message.guild, member,
                                self.timeout_title.format(member.name),
                                self.timeout_msg.format(member.name,
                                                        ctx.message.author.name,
                                                        seconds),
                                discord.Colour.red(),
                                "Timeout")

        async def msg_thing2():
            await mod_utils.mod(self.mod_channel_name, ctx.message.guild, member,
                                self.untimeout_title.format(member.name),
                                self.untimeout_msg.format(member.name),
                                discord.Colour.red(),
                                "Timeout (Over)")
        guild = ctx.message.guild
        role = discord.utils.find(
            lambda m: m.name == self.timeout_role, guild.roles)
        channel = discord.utils.find(
            lambda m: m.name == self.mod_channel_name, guild.text_channels)
        if role is None:
            try:
                await guild.create_role(name=self.timeout_role,
                                        colour=discord.Colour.red(),
                                        permissions=discord.Permissions(permissions=66560))
                role = discord.utils.find(
                    lambda m: m.name == self.timeout_role, guild.roles)
                try:
                    await member.add_roles(role)
                    if channel is not None:
                        await msg_thing()
                    await self.change_perms_text(guild, role, self.timeout_ow)
                    await self.change_perms_voice(guild, role, self.timeout_ow_vc)
                    await sleep(seconds)
                    await member.remove_roles(role)
                    if channel is not None:
                        await msg_thing2()
                except discord.Forbidden:
                    await ctx.send("I seem to have no permission to add roles to members.")
            except discord.Forbidden:
                await ctx.send("I seem to have no permission to create a timeout role.")
        else:
            try:
                await member.add_roles(role)
                if channel is not None:
                    await msg_thing()
                await self.change_perms_text(guild, role, self.timeout_ow)
                await self.change_perms_voice(guild, role, self.timeout_ow_vc)
                await sleep(seconds)
                await member.remove_roles(role)
                if channel is not None:
                    await msg_thing2()
            except discord.Forbidden:
                await ctx.send("I seem to have no permission to add roles to members.")

    @commands.command()
    async def auto_role(self, ctx, *, role: discord.Role):
        """Automatically adds roles to users when they join the server."""
        user = ctx.message.author
        guild = ctx.message.guild
        if user.guild_permissions.manage_roles is False:
            await ctx.send("You have no permission to add roles to the auto role list.")
            return

        with open(other_config, encoding='utf8') as file:
            data = json.load(file)

        thing = {
            guild.id: role.name
        }
        if data[str(guild.id)] is not None:
            data.pop(str(guild.id))
        data.update(thing)
        with open(other_config, 'w', encoding='utf8') as file:
            json.dump(data, file, indent=4)
        await ctx.send("Added role **{}** to the auto role list.").format(role)


def setup(bot):
    """adds the cog as a cog"""
    bot.add_cog(Moderation(bot))
