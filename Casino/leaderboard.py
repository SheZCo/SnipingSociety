import discord 
from discord.ext import commands
import json
import os

BALANCE_FILE = "casino_balances.json"

def load_data():
    if not os.path.isfile(BALANCE_FILE):
        return {}
    with open(BALANCE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}
    
class CasinoLeaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leaderboard", aliases=["lb"])
    async def Leaderboard(self, ctx):
        data = load_data()
        if not data:
            await ctx.send("📉 No one has a casino account yet.")
            return
        
            
        #Sort by descending balance
        top_balances = sorted(data.items(), key=lambda x: x[1], reverse = True)

        embed = discord.Embed(
            title="🏆 Casino Leaderboard",
            description="Top 5 Richest Snipers",
            color=discord.Color.gold()
        )

        for i, (user_id, info) in enumerate(top_balances[:5], start=1):
            user = await self.bot.fetch_user(int(user_id))
            balance = info.get("balance", 0)
            wins = info.get("wins", 0)
            embed.add_field(
                name=f"#{i} - {user.name}",
                value=f"💰 {balance} coins\n🏅 {wins} wins",  # <-- Added wins display
                inline=False
            )
        embed.set_footer(text="🤑 SnipingSociety | Flex harder. 🤑")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CasinoLeaderboard(bot))

