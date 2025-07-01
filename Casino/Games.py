import discord
from discord.ext import commands
import os
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
        old_balance = balance
        Bank.set_balance(user_id, balance - amount)

        base_weights = {
            "🍒": 10,
            "🍋": 8,
            "🍊": 7,
            "🍉": 5,
            "⭐": 4,
            "7️⃣": 3
        }

        # 📈 Loss-based jackpot bias
        losses = Bank.get_loss_count(user_id)
        bonus = min(losses, 10)
        base_weights["⭐"] += bonus
        base_weights["7️⃣"] += bonus

        # 🎰 Weighted symbol pool
        weighted_symbols = [s for s, w in base_weights.items() for _ in range(w)]

        # 🎲 Rig system (15% chance to force win)
        rig_chance = 0.15
        rigged = random.random() < rig_chance
        if rigged:
           win_symbol = random.choice(weighted_symbols)
           win_row = random.randint(0, 2)
           grid = []
           for row in range(3):
               if row == win_row:
                   grid.append([win_symbol] * match_count)
               else: 
                     grid.append([random.choice(weighted_symbols) for _ in range(match_count)])
                  
        else:
            grid = [[random.choice(weighted_symbols) for _ in range(match_count)] for _ in range(3)]

        # 📊 Determine max matches in rows or columns
        max_matches = 0
        for row in grid:
            row_counts = {}
            for symbol in row:
                row_counts[symbol] = row_counts.get(symbol, 0) + 1
            max_matches = max(max_matches, max(row_counts.values()))

        for col in range(match_count):
            col_counts = {}
            for row in range(3):
                symbol = grid[row][col]
                col_counts[symbol] = col_counts.get(symbol, 0) + 1
            max_matches = max(max_matches, max(col_counts.values()))


        # 💰 Payout logic
        payout_multiplier = {2: 2, 3: 5, 4: 10}
        if max_matches >= match_count:
            winnings = amount * payout_multiplier[match_count]
            Bank.set_balance(user_id, Bank.get_balance(user_id) + winnings)
            Bank.set_loss_count(user_id, 0)
            color = discord.Color(0x00FFFF)
            result_text = f"🎉 Congrats! You got {max_matches} matching emojis and won {winnings} coins!"
        else:
            winnings = 0
            Bank.set_loss_count(user_id, losses + 1)
            color = discord.Color.red()
            result_text = "❌ No match. Better luck next time."
        
        
        new_balance = Bank.get_balance(user_id)
        diff = new_balance - old_balance
        percent_change = (diff / old_balance) * 100 if old_balance > 0 else 0
        emoji_color = "🟢" if diff > 0 else "🔴"
        sign = "+" if diff > 0 else "-"
        balance_change = f"{emoji_color} {sign}{abs(diff)} coins ({sign}{abs(percent_change):.1f}%)\n💰 Your new balance: **{new_balance} coins**."

        # 🎰 Display 3xN grid
        display = "\n".join([" | ".join(row) for row in grid])
        embed = discord.Embed(
            title="🎰 Slot Machine 🎰",
            description=f"{display}\n\n{result_text}",
            color=color
        )
        embed.add_field(name="💰 Balance Update", value=balance_change, inline=False)
        embed.set_footer(text=f"🎰 SnipingSociety | Played by {ctx.author.display_name}")
        await ctx.send(embed=embed)



    @casino.command()
    async def coinflip(self, ctx, side: str, amount: int):
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


