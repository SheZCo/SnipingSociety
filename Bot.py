#https://discord.com/developers/applications/1389069986948976750/oauth2
import discord
from discord.ext import commands
import re
import aiohttp

# Replace this with your actual token
TOKEN = ''

# Bot prefix (so commands start with ! or . or whatever you choose)
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'🚀 SnipingSociety Bot is live as {bot.user.name}')
    # On bot startup on terminal

# Simple Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send('🏹 Sniper Ready – Ping Confirmed')

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
        ca = found_ca.group()
        await message.channel.send(f"🔍 Fetching token info for `{ca}`...")
        
        async with aiohttp.ClientSession() as session:
            url = f'https://pump.fun/api/token/{ca}'
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()

                    name = data.get("name", "Unknown Token")
                    supply = data.get("supply", 0)
                    price = data.get("price", 0)
                    mc = data.get("market_cap", 0)
                    creator = data.get("creator", "N/A")

                    embed = discord.Embed(
                        title=f"📈 Token Info: {name}",
                        description=f"**Market Cap:** ${int(mc):,}\n**Price:** ${round(price, 6)}\n**Supply:** {int(supply):,}\n**Creator:** `{creator}`",
                        color=discord.Color.green()
                    )
                    embed.set_footer(text="SnipingSociety Bot")
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send("❌ Could not fetch data for that CA.")
    elif found_token:
        token = found_token.group()
        await message.channel.send(f"🔍 Searching for token named **{token}**...")
        # Placeholder: later we match token name to known CA via API (e.g. Pump.fun or Solana explorer)

    await bot.process_commands(message)  # important to keep command system working   
       
       

# Run the bot
bot.run(TOKEN)