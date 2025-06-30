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
                high = data.get('high')
                low= data.get('low')
                prev_close = data.get('pc')
                emoji = "🟢📈" if price_direction == "up" else "🔴📉"
                embedcolor = discord.Color.green() if price_direction == "up" else discord.Color.red()
                price_direction = "up" if current >= prev_close else "down"
                tradingview_url = f"https://www.tradingview.com/symbols/{ticker.upper()}/"
                
                ## API ERROR HANDLING
                if currentprice is None or high is None:
                    return f"❌ Sorry! We're experiencing Issues right now!"
                    
                # Calc Price Change
                percent_change - ((current - prev_close) / prev_close) * 100
                ##################
                
                embed = discord.Embed( 
                    title=f"{emoji} {ticker.upper()} Stock Info",
                    description=f"{ticker.upper()} Current Price: **${currentprice.2f} 🔗 [View Chart]({tradingview_url})"
                    color = embed_color
                )
                embed.add_field(name="📊 Todays High", value=" **${high:.2f}", inline=False)
                embed.add_field(name="📉 Today's Low", value="**${low:.2f}", inline=False)
                embed.add_field(name="📈 Percent Change", value="**{percent_change:+.2f}%**", inline=False)
                embed.set_footer(text="SnipingSociety | Stock Data via Finnhub")
                return embed
            else:
                @bot.event
                print(f"❌ Finnhub API failed.")