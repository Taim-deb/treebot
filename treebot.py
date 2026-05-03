import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

ALLOWED_ROLES = ["put-roles-allowed]


def has_allowed_role(user: discord.Member) -> bool:
    return any(role.name in ALLOWED_ROLES for role in user.roles)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="help", description="List all commands")
async def help_cmd(interaction: discord.Interaction):
    cmds = bot.tree.get_commands()

    embed = discord.Embed(
        title="Bot Commands",
        description="Here are all available commands:",
        color=discord.Color.blue()
    )

    for cmd in cmds:
        embed.add_field(
            name=f"/{cmd.name}",
            value=cmd.description or "No description",
            inline=False
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="hello", description="Say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}")


@bot.tree.command(name="kick", description="Kick a member")
@app_commands.describe(member="User to kick", reason="Reason for kick")
async def kick(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "No reason provided"
):
    if not has_allowed_role(interaction.user):
        return await interaction.response.send_message(
            "You are not allowed to use this command.",
            ephemeral=True
        )

    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member} was kicked. Reason: {reason}")


@bot.tree.command(name="ban", description="Ban a member")
@app_commands.describe(member="User to ban", reason="Reason for ban")
async def ban(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "No reason provided"
):
    if not has_allowed_role(interaction.user):
        return await interaction.response.send_message(
            "You are not allowed to use this command.",
            ephemeral=True
        )

    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member} was banned. Reason: {reason}")


@bot.tree.command(name="unban", description="Unban a user by name#tag")
@app_commands.describe(user="User in the form name#1234")
async def unban(interaction: discord.Interaction, user: str):
    if not has_allowed_role(interaction.user):
        return await interaction.response.send_message(
            "You are not allowed to use this command.",
            ephemeral=True
        )

    banned_users = await interaction.guild.bans()
    name, discrim = user.split("#")

    for ban_entry in banned_users:
        if (ban_entry.user.name, ban_entry.user.discriminator) == (name, discrim):
            await interaction.guild.unban(ban_entry.user)
            return await interaction.response.send_message(
                f"Unbanned {ban_entry.user}"
            )

    await interaction.response.send_message("User not found")


@bot.tree.command(name="mute", description="Mute a member")
@app_commands.describe(member="User to mute")
async def mute(interaction: discord.Interaction, member: discord.Member):
    if not has_allowed_role(interaction.user):
        return await interaction.response.send_message(
            "You are not allowed to use this command.",
            ephemeral=True
        )

    role = discord.utils.get(interaction.guild.roles, name="Muted")

    if not role:
        role = await interaction.guild.create_role(name="Muted")
        for channel in interaction.guild.channels:
            await channel.set_permissions(role, send_messages=False, speak=False)

    await member.add_roles(role)
    await interaction.response.send_message(f"{member} muted")


@bot.tree.command(name="unmute", description="Unmute a member")
@app_commands.describe(member="User to unmute")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    if not has_allowed_role(interaction.user):
        return await interaction.response.send_message(
            "You are not allowed to use this command.",
            ephemeral=True
        )

    role = discord.utils.get(interaction.guild.roles, name="Muted")

    if role:
        await member.remove_roles(role)
        await interaction.response.send_message(f"{member} unmuted")
    else:
        await interaction.response.send_message("Muted role not found")


@bot.tree.command(name="addrole", description="Give a role to a member")
@app_commands.describe(member="User to give the role to", role="Role to give")
async def addrole(
    interaction: discord.Interaction,
    member: discord.Member,
    role: discord.Role
):
    if not has_allowed_role(interaction.user):
        return await interaction.response.send_message(
            "You are not allowed to use this command.",
            ephemeral=True
        )

    await member.add_roles(role)
    await interaction.response.send_message(f"Added {role.name} to {member.name}")


@bot.tree.command(name="removerole", description="Remove a role from a member")
@app_commands.describe(member="User to remove the role from", role="Role to remove")
async def removerole(
    interaction: discord.Interaction,
    member: discord.Member,
    role: discord.Role
):
    if not has_allowed_role(interaction.user):
        return await interaction.response.send_message(
            "You are not allowed to use this command.",
            ephemeral=True
        )

    await member.remove_roles(role)
    await interaction.response.send_message(f"Removed {role.name} from {member.name}")


@bot.tree.command(name="announce", description="Send an announcement in this channel")
@app_commands.describe(message="Announcement text")
async def announce(interaction: discord.Interaction, message: str):
    if not has_allowed_role(interaction.user):
        return await interaction.response.send_message(
            "You are not allowed to use this command.",
            ephemeral=True
        )

    embed = discord.Embed(
        title="Message from admin",
        description=message,
        color=discord.Color.gold()
    )

    await interaction.response.send_message("Announcement sent.", ephemeral=True)
    await interaction.channel.send(embed=embed)

bot.run("discord-token-here")