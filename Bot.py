#https://discord.com/developers/applications/1389069986948976750/oauth2
import discord
from discord.ext import commands

# Replace this with your actual token
TOKEN = ''

# Bot prefix (so commands start with ! or . or whatever you choose)
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'🚀 SnipingSociety Bot is live as {bot.user.name}')

# Simple Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send('🏹 Sniper Ready – Ping Confirmed')

# Placeholder for future commands
@bot.command()
async def snipe(ctx):
    await ctx.send('🔍 CA scanner coming soon...')

# Run the bot
bot.run(TOKEN)