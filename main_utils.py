from dotenv import load_dotenv
from discord.ext import commands
from Casino import Bank
import discord
import aiohttp
import asyncio
import random
import re
import os


def has_roles(*role_names):
    async def predicate(ctx):
        user_roles = [role.name for role in ctx.author.roles]
        return any(role in user_roles for role in role_names)
    return commands.check(predicate)

def is_admin():
    admin_roles=['Owner', 'The Boys'] 
    return has_roles(*admin_roles)


class MainUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx, category: str = None, command: str = None):
        category = category.lower() if category else None
        command = command.lower() if command else None
        
        
        is_user_admin = False
        admin_roles = ['Owner', 'The Boys']
        user_roles = [role.name for role in ctx.author.roles]
        colorb = discord.Color(0x000000)
        if any(role in user_roles for role in admin_roles):
            is_user_admin = True
        
        aliases = {
            "stock": "stocks",
            "stocks": "stocks",
            "crypto": "crypto",
            "casino": "casino",
            "games": "casino",  # games maps to casino help
            "admin": "admin",
            "fun": "casino",    # if you want fun to map to casino as well
        }

        base_help_map = {
            "stocks": {
                "title": "📈 Stock Sniping Commands",
                "desc": "Commands related to stocks, options, and market analysis.",
                "color": discord.Color.blue(),
                "commands": {
                    "🔎 stock [ticker]": "Get live stock data.",
                    "📰 news [ticker]": "Recent news headlines.",
                    "📊 chart [ticker]": "Snapshot chart of stock price."
                },
                "footer": "SnipingSociety | Stock Sniping Set"
            },
            "crypto": {
                "title": "💰 Crypto Sniper Commands",
                "desc": "Catch pumpers, avoid rugs, and flip fast.",
                "color": discord.Color.orange(),
                "commands": {
                    "🔫 snipe dex {ca}": "Fetch token info from Dexscreener.",
                    "💎 trending": "Trending tokens and sniper plays (future)."
                },
                "footer": "SnipingSociety | Crypto Command Set"
            },
            "casino": {
                "title": "🎲 Casino & Games 🍒",
                "desc": "Test your luck or flex your bankroll.",
                "color": discord.Color.gold(),
                "commands": {
                    "🆕 start casino": "Create your casino account.",
                    "💰 balance": "View your coin balance.",
                    "📤 send {user} {amount}": "Send coins to another user.",
                    "🎰 slots {amount} [match]": "Spin the slots with optional match requirement.",
                    "🪙 coinflip {amount}": "Flip for 2x or lose it all."
                },
                "footer": "🎲 SnipingSociety | Casino & Games | Play smart, win big! 🎰"
            }
        }
        admin_help_map = {
            "admin": {
                "title": "😈 SnipingSociety Admin Prompt 😈",
                "desc": "Server management and alpha injection.",
                "color": colorb,
                "commands": {
                    "⚽ kick @user reason": "Kick a user from the server.",
                    "🛡️ ban @user reason length": "Ban a user from the server.",
                    "🎲 casinolytics Casino Dashboard": "Show casino analytics",
                    "🧠 injectalpha @user": "Upload sniper alpha into a user.",
                    "👔 coffeebreak": "Take a coffeebreak when things get too much",
                    "🧹 sweep...": "Delete recent messages.",
                    "🌈 rainbow @user": "Rainbow spam for wins.",
                    "💨 purge [amount]": "Bulk delete messages.",
                },
                "footer": "⛓️ SnipingSociety | Powered by @Sleutime | Precision builds power. Watch everything. ⛓️"
            },
            "stocks": {
                "title": "📈 Stock Sniping Commands",
                "desc": "Commands related to stocks, options, and market analysis.",
                "color": colorb,
                "commands": {
                    "🔎 stock [ticker]": "Get live stock data.",
                    "📰 news [ticker]": "Recent news headlines.",
                    "📊 chart [ticker]": "Snapshot chart of stock price."
                },
                "footer": "SnipingSociety | Stock Sniping Set"
            },
            "casino": {
                "title": "🎲 Admin Casino & Games 🍒",
                "desc": "Test your luck or flex your bankroll.",
                "color": colorb,
                "commands": {
                    "🆕 start casino": "Create your casino account.",
                    "💰 balance": "View your coin balance.",
                    "💲 addmoney {user} {amount}": "put money in someones pocket",
                    "📤 send {user} {amount}": "Send coins to another user.",
                    "🎰 slots {amount} [match]": "Spin the slots with optional match requirement.",
                    "🪙 coinflip {amount}": "Flip for 2x or lose it all.",
                },
                "footer": "🎲 SnipingSociety | Casino & Games | Play smart, win big! 🎰"
            },
            "crypto": {
                "title": "💰 Crypto Sniper Commands",
                "desc": "Catch pumpers, avoid rugs, and flip fast.",
                "color": colorb,
                "commands": {
                    "🔫 snipe dex {ca}": "Fetch token info from Dexscreener.",
                    "💎 trending": "Trending tokens and sniper plays (future)."
                },
                "footer": "SnipingSociety | Crypto Command Set"
            },
            **base_help_map
        }
        current_map = admin_help_map if is_user_admin else base_help_map

        if category is None:
            if is_user_admin:
                embed = discord.Embed(
                title="🛡️ SnipingSociety Admin Help",
                description="Control panel for SnipingSociety | `.help [category]` for commands.",
                color=colorb
                )
                embed.add_field(name="📈 .help stocks", value="Commands for sniping stocks/options.", inline=False)
                embed.add_field(name="💰 .help crypto", value="Crypto, sniping, flipping tools.", inline=False)
                embed.add_field(name="🎲 .help casino", value="Casino games & coin tracking.", inline=False)
                embed.add_field(name="😈 .help admin", value="Bot admin & utility commands.", inline=False)
                embed.set_footer(text="SnipingSociety Admin | Move smart. Win harder.")
            else:
                embed = discord.Embed(
                title="🛡️ SnipingSociety Bot Help",
                description="Type `.help [category]` to view commands in that area.",
                color=discord.Color.dark_purple()
                )
                embed.add_field(name="📈 .help stocks", value="Commands for sniping stocks/options.", inline=False)
                embed.add_field(name="💰 .help crypto", value="Crypto, sniping, flipping tools.", inline=False)
                embed.add_field(name="🎲 .help casino", value="Casino games & coin tracking.", inline=False)
                embed.set_footer(text="SnipingSociety | Stay sharp, stay profitable ⚡")
            await ctx.send(embed=embed)
            return
    
        category = aliases.get(category, category)
        if is_user_admin and category in admin_help_map:
            data = admin_help_map[category]
        else:
            data = base_help_map.get(category)

        if data:
            data = current_map[category]
            embed = discord.Embed(
                title=data["title"],
                description=data["desc"],
                color=data["color"]
            )
            for cmd, desc in data["commands"].items():
                embed.add_field(name=cmd, value=desc, inline=False)
            embed.set_footer(text=data.get("footer", "SnipingSociety | Stay sharp, stay profitable ⚡"))
            await ctx.send(embed=embed)
            

######### ADMIN SHIT ###########

    @commands.command(name="injectalpha")
    @is_admin()
    async def InjectAlpha(self, ctx):

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
    async def InjectAlpha_error(self, ctx, error):
        if isinstance(error, commands.CkeckFailure):
            await ctx.send("🚫 You don’t have the clearance to inject alpha.")


    @commands.command(name="coffeebreak")
    @is_admin()
    async def coffeebreak(self, ctx):
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

    @commands.command(name="sweep")
    @is_admin()
    async def sweep(self, ctx, amount: int=10):
        await ctx.channel.purge(limit=amount)
        confirmation = await ctx.send(f"🧹 Let's forget about that... 🤔")

    @commands.command(name="purge")
    @is_admin()
    async def purge(self, ctx, amount: int):
        if amount is None:
            await ctx.send(f"🧹 Example usage '.purge 1-100'")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        confirmation = await ctx.send(f"🧹 Deleted {len(deleted) - 1} messages.")
        await confirmation.delete(delay=3)  # Remove confirmation after 3 seconds


    @commands.command(name="rainbow")
    @is_admin()
    async def rainbowwins(self, ctx, target: discord.Member):
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
                description=f"🔥 {target.mention} is the chosen sniper!",
                color=color
            )
            embed.add_field(name=f"🌈 BIG MONEY BIG MONEY 🌈", value=f"YOU WIN", inline=False)
            embed.set_footer(text=f"SnipingSociety | Premium Sniper | {target.display_name}")
            await ctx.send(embed=embed)
            await asyncio.sleep(0.5)
    @rainbowwins.error
    async def rainbowerror(self, ctx,error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"🌈 Not FOR YOU 🌈")

    @commands.command(name="casinolytics")
    @is_admin()
    async def casino_analytics(self, ctx):
        """Show casino analytics dashboard for admins."""
        data = Bank.load_data()
        total_players = len(data)
        if total_players == 0:
            await ctx.send("⚠️ No casino accounts found.")
            return
        
        total_coins = sum(user.get("balance", 0) for user in data.values())
        total_losses = sum(user.get("losses", 0) for user in data.values())
        total_wins = sum(user.get("wins", 0) for user in data.values())
        avg_balance = total_coins / total_players if total_players else 0

        embed = discord.Embed(
            title="🎲 Admin Casino Analytics Dashboard",
            description=f"Admin overview of casino economy & player stats.",
            color=discord.Color(0x000000)
        )
        embed.add_field(name="👥 Total Players", value=str(total_players), inline=True)
        embed.add_field(name="💰 Total Coins in Circulation", value=f"{total_coins:,}", inline=True)
        embed.add_field(name="📊 Average Player Balance", value=f"{avg_balance:,.2f}", inline=True)
        embed.add_field(name="📉 Total Losses Recorded", value=str(total_losses), inline=True)
        embed.add_field(name="🏅 Total Wins Recorded", value=str(total_wins), inline=True)  # <-- Added field for wins
        embed.set_footer(text="🎲 SnipingSociety | Casino Analytics")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MainUtils(bot))