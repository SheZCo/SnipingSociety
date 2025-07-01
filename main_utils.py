from dotenv import load_dotenv
from discord.ext import commands
import discord
import aiohttp
import asyncio
import random
import re
import os

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

def has_roles(*role_names):
    async def predicate(ctx):
        user_roles = [role.name for role in ctx.author.roles]
        return any(role in user_roles for role in role_names)
    return commands.check(predicate)

def is_admin():
    admin_roles=['Owner', 'The Boys'] 
    return has_roles(*admin_roles)


def setup_commands(bot):
    @bot.command(name="help")
    async def help(ctx, topic: str = None):
        user_roles = [role.name for role in ctx.author.roles]
        admin_roles = ["Owner", "The Boys"]
        
        if topic is None:
            embed = discord.Embed(
                title="🛡️ SnipingSociety Bot Help",
                description="Type `.help [category]` to view commands in that area.",
                color=discord.Color.dark_purple()
            )
            embed.add_field(name="📈 .help stocks", value="Commands for sniping stocks/options.", inline=False)
            embed.add_field(name="💰 .help crypto", value="Crypto, sniping, flipping tools.", inline=False)
            embed.add_field(name="😎 .help fun", value="Crypto, sniping, flipping tools.", inline=False)
            embed.set_footer(text="SnipingSociety | Stay sharp, stay profitable ⚡")
            await ctx.send(embed=embed)

        elif topic.lower() == "stocks":
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

        elif topic.lower() == "admin":
            admin_roles = ['Owner', 'The Boys']
            user_roles = [role.name for role in ctx.author.roles]
            print("[DEBUG] Your roles:", [role.name for role in ctx.author.roles])
            if any(role in user_roles for role in admin_roles):
                embed = discord.Embed(
                    title="😈 SnipingSociety Admin Prompt 😈",
                    description=" ",
                    color=discord.Color(0x000000)
                )
                embed.add_field(name="⚽ .kick", value="Kick a user from the server.")
                embed.add_field(name="🛡️ .ban", value="Ban a user from the server.")
                embed.add_field(name="🌈 RAINBOW WINS", value="Some colorful alpha.")
                embed.add_field(name="🧹 Sweep...", value="Cleans the mess, deletes last 10 messages, or use purge")
                embed.add_field(name="🧠 Inject Alpha", value="Injects top-tier sniper wisdom directly into your brain.")
                embed.add_field(name="👔 Coffee Break", value="Posts a chill gif and says youll be back")
                embed.set_footer(text="⛓️ SnipingSociety | Powered by @Sleutime ⛓️ Precision builds power. Watch everything.")  
                await ctx.send(embed=embed)   



######### ADMIN SHIT ######
    @bot.command(name="injectalpha")
    @is_admin()
    async def InjectAlpha(ctx):

        if not ctx.message.mentions:
            await ctx.send("❌ Tag someone to inject alpha into. Example: `.injectalpha @user`")
            return
        
        target = ctx.message.mentions[0]
        alpha_quotes = [
            f"🧬 Alpha Upload Complete: {target.mention} now sees liquidity before it’s even added.",
            f"📡 {target.mention} can smell rugs before the dev even hits Deploy.",
            f"🔍 {target.mention} just unlocked private snipes on coins that don’t exist yet.",
            f"⚙️ {target.mention} runs so many scanners their Discord lags IRL.",
            f"💾 {target.mention} downloaded the entire blockchain into RAM.",
            f"🚀 {target.mention} gets alerts before the dev even writes the token name."
        ]
        await ctx.send(random.choice(alpha_quotes))

    @InjectAlpha.error
    async def InjectAlpha_error(ctx, error):
        if isinstance(error, commands.CkeckFailure):
            await ctx.send("🚫 You don’t have the clearance to inject alpha.")

###########################################
    @bot.command(name="coffebreak")
    @is_admin()
    async def coffebreak(ctx):
        coffee_quotes = [
            "☕ Taking a break from the rugs. Be back when liquidity looks safer.",
            "🧘‍♂️ Admin is meditating on the next 100x. Do not disturb.",
            "🥱 All that sniping drained me. Time for a brew.",
            "📉 Coffee > Charts. At least for the next 10 minutes.",
            "💤 Manifesting green candles with espresso shots.",
            "😮‍💨 The dev can wait. My caffeine can’t."
        ]

        coffee_gifs = [
            "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
            "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
            "https://media.giphy.com/media/jkZtSdwKOx05BOlapR/giphy.gif",
            "https://media.giphy.com/media/l2JJKs3I69qfaQleE/giphy.gif"
        ]
        foot_quotes = [
            "Fueling the grind, one shot at a time.",
            "Powered by caffeine and hustle.",
            "Where alpha meets espresso.",
            "Stay sharp. Sip sharper.",
            "Injecting alpha, one brew at a time.",
            "Brewed for champions.",
            "Grinding harder than your morning coffee.",
            "Espresso your alpha mindset.",
            "Stay alert, stay alpha.",
        ]
        quote = random.choice(coffee_quotes)
        gif = random.choice(coffee_gifs)

        embed = discord.Embed(
            title="☕ Admin Coffee Break",
            description=quote,
            color=0x6f4e37
        )
        embed.set_image(url=gif)
        footing = random.choice(foot_quotes)
        embed.set_footer(text=f"😈 SnipingSociety 📈 | {footing}")
        await ctx.send(embed=embed)

    @coffebreak.error
    async def Coffee_error(ctx, error):
        if isinstance(error, commands.CkeckFailure):
            await ctx.send(f"🚫 You don't need any more coffee...")
#########################

    @bot.command(name="sweep")
    @is_admin()
    async def sweep(ctx, amount: int=10):
        await ctx.channel.purge(limit=amount)
        confirmation = await ctx.send(f"🧹 Let's forget about that...\n 🤔")

    @bot.command(name="purge")
    @is_admin()
    async def purge(ctx, amount: int):
        if amount is None:
            await ctx.send(f"🧹 Example usage '.purge 1-100'")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        confirmation = await ctx.send(f"🧹 Deleted {len(deleted) - 1} messages.")
        await confirmation.delete(delay=3)  # Remove confirmation after 3 seconds
######################################

    @bot.command(name="rainbow")
    @is_admin()
    async def rainbowwins(ctx, target: discord.Member):
        RAINBOW_COLORS = [
            0xFF0000,  # Red
            0xFF7F00,  # Orange
            0xFFFF00,  # Yellow
            0x7FFF00,  # Chartreuse Green
            0x00FF00,  # Green
            0x00FF7F,  # Spring Green
            0x00FFFF,  # Cyan
            0x007FFF,  # Azure
            0x0000FF,  # Blue
            0x7F00FF,  # Violet
            0xFF00FF,  # Magenta
            0xFF007F,  # Rose
            0xFF1493,  # Deep Pink
            0xC71585   # Medium Violet Red
        ]
        for i, color in enumerate(RAINBOW_COLORS, start=1):
            embed = discord.Embed(
                title=f"🌈 BIG SNIPES BIG SNIPES 🌈",
                color=color
            )
            embed.add_field(name=f"🌈 BIG MONEY BIG MONEY 🌈", inline=False)
            embed.add_field(name=f"🌈{target.mention}🌈", inline=False)
            embed.add_field(name=f"🌈 BIG MONEY BIG MONEY 🌈", inline=False)
            embed.set_footer(text=f"SnipingSociety | Premium Sniper {target.display_name}")
            await ctx.send(embed=embed)
            await asyncio.sleep(0.5)
    @rainbowwins.error
    async def rainbowerror(ctx,error):
        if isinstance(error, commands.CkeckFailure):
            await ctx.send(f"🌈 Not FOR YOU 🌈")