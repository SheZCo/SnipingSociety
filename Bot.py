# SnipingSociety Pump Token Scanner Bot (Dexscreener Edition)

import discord
from discord.ext import commands
import re
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.command()
async def ping(ctx):
    await ctx.send('🏹 Sniper Ready – Ping Confirmed')

@bot.event
async def on_ready():
    print(f'🚀 SnipingSociety Bot is live as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    contract_address_pattern = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}(pump)?\b'
    found_ca = re.search(contract_address_pattern, message.content)

    if found_ca:
        ca_raw = found_ca.group().lower()
        ca = ca_raw[:-4] if ca_raw.endswith("pump") else ca_raw

        print(f"[📡] CA Detected: {ca}")
        await message.channel.send(f"🔍 Scanning `{ca}` on Dexscreener...")

        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{ca}"
                async with session.get(url) as resp:
                    print(f"[🌐] Dexscreener Status: {resp.status}")
                    if resp.status == 200:
                        data = await resp.json()
                        pair_data = data.get("pair", None)

                        if pair_data:
                            name = pair_data.get("baseToken", {}).get("name", "Unknown")
                            price = pair_data.get("priceUsd", "N/A")
                            market_cap = pair_data.get("marketCapUsd", "N/A")
                            liquidity = pair_data.get("liquidity", {}).get("usd", "N/A")
                            tx_count = pair_data.get("txCount", {}).get("h1", 0)
                            url_link = pair_data.get("url", "https://dexscreener.com/")

                            embed = discord.Embed(
                                title=f"📈 {name} – Token Stats",
                                description=(
                                    f"**💰 Price:** ${price}\n"
                                    f"**📊 Market Cap:** ${market_cap}\n"
                                    f"**💧 Liquidity:** ${liquidity}\n"
                                    f"**🔥 1h TXs:** {tx_count}\n"
                                    f"[🔗 View on Dexscreener]({url_link})"
                                ),
                                color=discord.Color.green()
                            )
                            embed.set_footer(text="SnipingSociety Bot | Powered by Dexscreener")
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send("⚠️ No token data found. Might not be trading yet.")
                    else:
                        await message.channel.send("❌ Failed to reach Dexscreener API.")
        except Exception as e:
            print(f"[🔥] API Error: {e}")
            await message.channel.send("⚠️ Error while fetching token info.")

    await bot.process_commands(message)
