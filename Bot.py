# SnipingSociety Pump Token Scanner Bot (Dexscreener Edition)

from dotenv import load_dotenv
from discord.ext import commands
import stock_utils
from main_utils import setup_commands
import discord
import aiohttp
import re
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
main_utils.setup_(bot) ## Help / Primary bot uses




@bot.command()
async def stock(ctx, ticker: str):
    message = await stock_utils.fetch_stock_price(ticker.upper())
    await ctx.send(message)

    
 


@bot.event
async def on_ready():
    print(f'🚀 SnipingSociety Bot is live as {bot.user.name}')

bot.run(TOKEN)