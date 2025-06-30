from dotenv import load_dotenv
from discord.ext import commands
import discord
import aiohttp
import re
import os

API_KEY = os.getenv("FINN_API")

async def fetch_stock_price(ticker):
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                price = data.get('c')
                return f"💹 {ticker.upper()} – ${price}" if price else "❌ No price found."
            else:
                return f"❌ Finnhub API failed."