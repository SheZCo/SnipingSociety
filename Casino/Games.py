import discord
from discord.ext import commands
import random
from . import Bank

class CasinoGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def casino(self, ctx):
        # If user runs .casino without any subcommand
        await ctx.send("🎲 Available casino commands: `slots`, `coinflip`.\nTry `.casino slots {amount}`")

    @casino.command()
    async def slots(self, ctx, amount: int, match_count: int = 3):
        user_id = ctx.author.id
        if amount <=0:
            await ctx.send("❌ Amount must be positive.")
            return
            
        if match_count not in [2, 3, 4]:
            await ctx.send("❌ You can only bet on 2, 3, or 4 matching emojis.")
            return 
            
        balance=Bank.get_balance(user_id)
        if balance < amount:
            await ctx.send(f"❌ You don’t have enough coins to bet {amount}. Your balance: {balance}")
            return
            
        #Deduct Bet
        Bank.set_balance(user_id, balance - amount)

        #spin upto 4 emojis for 4 matches
        symbols = ["🍒", "🍋", "🍊", "🍉", "⭐", "7️⃣"]
        result = [random.choice(symbols) for _ in range(3)]
            
        embed = discord.Embed(
            title="🎰 Slot Machine 🎰",
            description=f"{' | '.join(result)}",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

        # Count max matching emojis
        counts = {}
        for emoji in result:
            counts[emoji] = counts.get(emoji, 0) + 1
        max_matches = max(counts.values())

        #Payout 
        if max_matches >= match_count:
            payout_multiplier = {2: 2, 3: 5, 4: 10}
            winnings = amount * payout_multiplier[match_count]
            await ctx.send(f"🎉 Congrats! You got {max_matches} matching emojis and won {winnings} coins!")
            Bank.set_balance(user_id, Bank.get_balance(user_id) + winnings)
        else: 
            await ctx.send("Better luck next time")


    @casino.command()
    async def casinoflip(self, ctx, side: str, amount: int):
        user_id = ctx.author.id
        side = side.lower()

        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return
            
        if side not in ["heads", "tails"]:
            await ctx.send("❌ Please choose either `heads` or `tails`.")
            return
        balance = Bank.get_balance(user_id)
        if balance < amount:
            await ctx.send(f"❌ You don’t have enough coins. Your balance: {balance}")
            return
        Bank.set_balance(user_id, balance - amount)
        result = random.choice(["heads", "tails"])
        win = side == result

        if win:
            winnings = amount * 2
            Bank.set_balance(user_id, Bank.get_balance(user_id) + winnings)
            outcome = f"✅ It's **{result.upper()}**! You won **{winnings} coins**!"
            color = discord.Color.green()
        else:
            outcome = f"❌ It's **{result.upper()}**. You lost your bet."
            color = discord.Color.red()

        embed = discord.Embed(
            title="🪙 Coinflip",
            description=outcome,
            color=color
        )
        embed.set_footer(text="SnipingSociety | Casino & Games | Flip smart.")
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(CasinoGames(bot))


