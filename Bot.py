#https://discord.com/developers/applications/1389069986948976750/oauth2
import discord
from discord.ext import commands
import re
import aiohttp
import os
from dotenv import load_dotenv

# Replace this with your actual token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot prefix (so commands start with ! or . or whatever you choose)
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
# Simple Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send('🏹 Sniper Ready – Ping Confirmed')
@bot.event
async def on_ready():
    print(f'🚀 SnipingSociety Bot is live as {bot.user.name}')
    # On bot startup on terminal
    
    
# Token Scanning Pumpfun Api implementation
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
        
    # Regex Patterns for Tokens
    contract_address_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'
    token_name_pattern = r'\$[A-Za-z0-9]{2,10}'

    found_ca = re.search(contract_address_pattern, message.content)
    found_token = re.search(token_name_pattern, message.content)

    if found_ca:
    ca_raw = found_ca.group().lower()
    if ca_raw.endswith("pump"):
        ca = ca_raw[:-4]
    else:
        ca = ca_raw

    print(f"[📡] CA Detected: {ca}")
    await message.channel.send(f"🔍 Fetching token info for `{ca}`...")

    try:
        async with aiohttp.ClientSession() as session:
            url = f'https://api.pumpfunapi.org/token/{ca}'
            async with session.get(url) as resp:
                print(f"[🌐] API Status: {resp.status}")
                content = await resp.text()
                print(f"[📬] API Response: {content[:300]}...")  # limit preview

                if resp.status == 200:
                    data = await resp.json()

                    name = data.get("name", "Unknown")
                    price = data.get("price", 0)
                    market_cap = data.get("marketCap", 0)
                    supply = data.get("totalSupply", 0)
                    creator = data.get("creator", "N/A")
                    rug_status = data.get("rugged", False)

                    embed = discord.Embed(
                        title=f"📈 {name} – Token Info",
                        description=(
                            f"**💰 Market Cap:** ${int(market_cap):,}\n"
                            f"**💎 Price:** ${round(price, 6)}\n"
                            f"**🧬 Supply:** {int(supply):,}\n"
                            f"**👨‍💻 Creator:** `{creator}`\n"
                            f"**🚨 Rugged:** {'Yes ❌' if rug_status else 'No ✅'}"
                        ),
                        color=discord.Color.red() if rug_status else discord.Color.green()
                    )
                    embed.set_footer(text="SnipingSociety Bot | Live from PumpFunAPI.org")
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("❌ Could not fetch data for that CA.")
    except Exception as e:
        print(f"[🔥] API Error: {e}")
        await message.channel.send("⚠️ API error occurred while fetching token info.")

    elif found_token:
        token = found_token.group()
        await message.channel.send(f"🔍 Searching for token named **{token}**...")
        # Placeholder: later we match token name to known CA via API (e.g. Pump.fun or Solana explorer)

    await bot.process_commands(message)  # important to keep command system working   
       
       

# Run the bot
bot.run(TOKEN)