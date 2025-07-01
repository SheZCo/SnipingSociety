# SnipingSociety Pump Token Scanner Bot (Dexscreener Edition)

from dotenv import load_dotenv
from discord.ext import commands
from Casino import Bank, Games, leaderboard
import stock_utils
import main_utils
import discord
import aiohttp
import asyncio
from colorama import init, Fore, Style
import re
import os


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
bot.remove_command('help')

@bot.command(name="stock")
async def Stockprice(ctx, ticker: str):
    SP = await stock_utils.fetch_stock_price(ticker.upper())
    if isinstance(SP, discord.Embed): 
        await ctx.send(embed=SP)
    else:
        await ctx.send(f"❌ Sorry! We're experiencing Issues right now!")

@bot.event
async def on_ready():
    print(f'🚀 SnipingSociety Bot is live as {bot.user.name}\n')
    print(f'STOCK FINN API KEY: ' + os.getenv("FINN_API"))

async def main():
    try:
        await bot.load_extension("maint_utils.MainUtils")
        await bot.load_extension("Casino.Bank")
        await bot.load_extension("Casino.Games")
        await bot.load_extension("Casino.leaderboard")
    except Exception as e:
        print(f"Failed to load: {e}")
    print(f'🧠 Starting bot...')
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())


