from dotenv import load_dotenv
from discord.ext import commands
import discord
import aiohttp
import re
import os




async def fetch_stock_price(ticker):
    API_KEY = os.getenv("FINN_API")
    url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                
                data = await response.json()
                
                currentprice = data.get('c')
                high = data.get('h')
                low= data.get('l')
                prev_close = data.get('pc')
                
                price_direction = "up" if currentprice >= prev_close else "down"
                embedcolor = discord.Color.green() if price_direction == "up" else discord.Color.red()
                emoji = "🟢" if price_direction == "up" else "🔴"
                tradingview_url = f"https://www.tradingview.com/symbols/{ticker.upper()}/"
                
                ## API ERROR HANDLING
                if currentprice is None or high is None:
                    return f"❌ Sorry! We couldn't find data for {ticker}"
                    
                # Calc Price Change
                percent_change = ((currentprice - prev_close) / prev_close) * 100
                ##################
                
                embed = discord.Embed( 
                    title=f"{emoji} {ticker.upper()} Stock Info",
                    description=f"{ticker.upper()} Current Price: **${currentprice:.2f} 🔗 [View Chart]({tradingview_url})",
                    color = embedcolor
                )
                embed.add_field(name="📊 Todays High", value=f"**${high:.2f}", inline=False)
                embed.add_field(name="📉 Today's Low", value=f"**${low:.2f}", inline=False)
                embed.add_field(name="📈 Percent Change", value=f"**{percent_change:+.2f}%**", inline=False)
                embed.set_footer(text="SnipingSociety | Stock Data via Finnhub")
                return embed
            else:
                return f"❌ Sorry! We're experiencing Issues right now!"