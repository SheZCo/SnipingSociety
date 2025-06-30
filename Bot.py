# SnipingSociety Pump Token Scanner Bot (Dexscreener Edition)

from dotenv import load_dotenv
from discord.ext import commands
import stock_utils
import main_utils
import discord
import aiohttp
import re
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
bot.remove_command('help')

try:
    main_utils.setup_commands(bot)
except Exception as e:
    print(f"{e}")


@bot.command()
async def stockprice(ctx, ticker: str):
    embed = await stock_utils.fetch_stock_price(ticker.upper())
    if embed: 
        await ctx.send(embed)
    else:
        await ctx.send(f"❌ Sorry! We're experiencing Issues right now!")




@bot.event
async def on_ready():
    print(f'🚀 SnipingSociety Bot is live as {bot.user.name}')
    print(f'FINN API KEY: ',os.getenv("FINN_API"))

bot.run(TOKEN)