# SnipingSociety Pump Token Scanner Bot (Dexscreener Edition)

from dotenv import load_dotenv
from discord.ext import commands
import stock_utils
import main_utils
import discord
import aiohttp
from colorama import init, Fore, Style
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


@bot.command(name="stock")
async def Stockprice(ctx, ticker: str):
    SP = await stock_utils.fetch_stock_price(ticker.upper())
    if SP: 
        await ctx.send(embed)
    else:
        await ctx.send(f"❌ Sorry! We're experiencing Issues right now!")

print(Fore.RED + f'🧠 Starting bot...')
@bot.event
async def on_ready():
    print(colorama.fore.GREEN + f'🚀 SnipingSociety Bot is live as {bot.user.name}\n' + Style.RESET_ALL)
    print(f'FINN API KEY: ' + colorama.Fore.CYAN + os.getenv("FINN_API") + colorama.STYLE.RESET_ALL)

bot.run(TOKEN)
