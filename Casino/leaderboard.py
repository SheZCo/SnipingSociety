import discord 
from discord.ext import commands
import json
import os

BALANCE_FILE = "casino_balances.json"

def load_balances():
    if not os.path.isfile(BALANCE_FILE):
        return {}
    with open(BALANCE_FILE, "r") as f:
        return json.load(f)
    
class CasinoLeaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @commands.command(name="leaderboard", aliases=["lb"])
        async def Leaderboard(self, ctx):
            balances = load_balances()
            if not balances:
                await ctx.send("📉 No one has a casino account yet.")
                return
            top_balances = sorted(balances.items(), key=lambda x: x[1], reverse = True)
            
            #Sort by descending balance
            embed = discord.Embed(
                title="🏆 Casino Leaderboard",
                description="Top 5 Richest Snipers",
                color=discord.Color.gold()
            )

            for i, (user_id, balance) in enumerate(top_balances, start=1):
                user = await self.bot.fetch_user(int(user_id))
                embed.add_field(name=f"#{i} - {user.name}", value=f"💰 {balance} coins", inline=False)

            embed.set_footer(text="🤑 SnipingSociety | Flex harder. 🤑")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CasinoLeaderboard(bot))

