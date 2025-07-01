from dotenv import load_dotenv
from discord.ext import commands
import discord
import aiohttp
import re
import os

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())




def setup_commands(bot):
    @bot.command(name="help")
    async def help(ctx, topic: str = None):
        if topic is None:
            embed = discord.Embed(
                title="🛡️ SnipingSociety Bot Help",
                description="Type `.help [category]` to view commands in that area.",
                color=discord.Color.dark_purple()
            )
            embed.add_field(name="📈 .help stocks", value="Commands for sniping stocks/options.", inline=False)
            embed.add_field(name="💰 .help crypto", value="Crypto, sniping, flipping tools.", inline=False)
            embed.add_field(name="🌹 .ping", value="Check if the bot is online and ready.", inline=False)
            embed.add_field(name="🧹 .purge", value="Clear messages in a channel.", inline=False)
            embed.set_footer(text="SnipingSociety | Stay sharp, stay profitable ⚡")
            await ctx.send(embed=embed)

        elif topic.lower() == "stocks" or "stock":
            embed = discord.Embed(
                title="📈 Stock Sniping Commands",
                description="Commands related to stocks, options, and market analysis.",
                color=discord.Color.blue()
            )
            embed.add_field(name="🔎 .stock {ticker}", value="Get live stock data.", inline=False)
            embed.add_field(name="📰 .news {ticker}", value="Recent news headlines.", inline=False)
            embed.add_field(name="📊 .chart {ticker}", value="Snapshot chart of stock price.", inline=False)
            embed.add_field(name="💡 More coming soon!", value="More tools on the way.", inline=False)
            embed.set_footer(text="SnipingSociety | Stock Sniping Set")
            await ctx.send(embed=embed)

        elif topic.lower() == "crypto":
            embed = discord.Embed(
                title="💰 Crypto Sniper Commands",
                description="Catch pumpers, avoid rugs, and flip fast.",
                color=discord.Color.gold()
            )
            embed.add_field(name="🔫 .snipe dex {ca}", value="Fetch token info from Dexscreener.", inline=False)
            embed.add_field(name="💎 .gems", value="Trending tokens and sniper plays (future).", inline=False)
            embed.add_field(name="💡 More coming soon!", value="More sniper tools soon.", inline=False)
            embed.set_footer(text="SnipingSociety | Crypto Command Set")
            await ctx.send(embed=embed)
        
        
    ##PURGE COMMAND
    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(ctx, amount: int):
        if amount < 1 or amount > 100:
            await ctx.send("❌ Please provide a number between 1 and 100.")
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        confirm = await ctx.send(f"🧹 Purged {len(deleted)-1} messages!")
        await confirm.delete(delay=5)

    ## PING PROMPT ? BOT UP
    @bot.command()
    async def ping(ctx):
        latency = bot.latency * 1000 # Convert to milliseconds
        await ctx.send(f"🌹 Sniper Ready – Ping Confirmed {latency:.2f}ms 🥀")