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
    main_utils.setup_commands()
except Exception as e:
    print(f"{e}")


@bot.command()
async def stock(ctx, ticker: str):
    message = await stock_utils.fetch_stock_price(ticker.upper())
    await ctx.send(message)

    
 


@bot.event
async def on_ready():
    print(f'🚀 SnipingSociety Bot is live as {bot.user.name}')

bot.run(TOKEN)