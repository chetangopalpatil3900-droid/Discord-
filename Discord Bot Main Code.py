import os
import discord
from discord.ext import commands
from discord import app_commands

# 1. Enable All Required Gateway Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# Initialize Bot with Command Prefix and Intents
bot = commands.Bot(command_prefix="!", intents=intents)

# 2. Event: When Bot is Ready and Online
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("--------------------------------------------------")
    
    # Automatically Sync Slash Commands to Discord API
    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} Slash Command(s) globally!")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

# 3. Slash Command Example 1: /ping
@bot.tree.command(name="ping", description="Replies with Pong and shows bot latency!")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! Latency: **{latency}ms**")

# 4. Slash Command Example 2: /hello
@bot.tree.command(name="hello", description="Greets the user!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}! Welcome to the server 👋")

# 5. Slash Command Example 3: /userinfo
@bot.tree.command(name="userinfo", description="Displays information about a user")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    
    embed = discord.Embed(
        title=f"User Info - {member.name}",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Username", value=str(member), inline=True)
    embed.add_field(name="User ID", value=str(member.id), inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
    
    await interaction.response.send_message(embed=embed)

# 6. Slash Command Example 4: /clear (Purge messages)
@bot.tree.command(name="clear", description="Deletes a specified number of messages (Admin only)")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    if amount < 1:
        await interaction.response.send_message("Please specify a number greater than 0.", ephemeral=True)
        return
        
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"✅ Successfully deleted {len(deleted)} message(s).")

# Error Handling for Missing Permissions
@clear.error
async def clear_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)

# 7. Start the Bot using BOT_TOKEN from Environment Variables or directly
TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

if __name__ == "__main__":
    bot.run(TOKEN)