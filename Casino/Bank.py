import discord 
from discord.ext import commands
import json
import os

BALANCE_FILE = "casino_balances.json"
INITIAL_BALANCE = 1000

def has_roles(*role_names):
    async def predicate(ctx):
        user_roles = [role.name for role in ctx.author.roles]
        return any(role in user_roles for role in role_names)
    return commands.check(predicate)

def is_admin():
    admin_roles=['Owner', 'The Boys'] 
    return has_roles(*admin_roles)

def load_balances():
    if not os.path.isfile(BALANCE_FILE):
        return {}
    with open(BALANCE_FILE, "r") as f:
        return json.load(f)
    
def save_balances(balances):
    with open(BALANCE_FILE, "w") as f:
        json.dump(balances, f, indent=4)

def get_balance(user_id, amount):
    balances = load_balances()
    balances[str(user_id)] = amount
    save_balances(balances)

def set_balance(user_id, amount):
    balances = load_balances()
    balances[str(user_id)] = amount
    save_balances(balances)

def has_account(user_id):
    balances = load_balances()
    return str(user_id) in balances

class CasinoBalance(commands.Cog):
    def __init__(self, bot):
        self.bot=bot


        @commands.command()
        async def start(self, ctx, *, arg=None):
            if arg is None:
                await ctx.send("❌ Please specify what to start. Try `.start casino`")
                return
            if arg.lower() == "casino":
                user_id = ctx.author.id
                if has_account(user_id):
                    await ctx.send(f"⚠️ {ctx.author.mention}, you already have a casino account!")
                    return
                ##ELSE
                set_balance(user_id, INITIAL_BALANCE)
                await ctx.send(f"🎉 {ctx.author.mention}, your casino account is ready! You received {INITIAL_BALANCE} coins.")
            else: 
                await ctx.send("❌ Unknown start option. Try `.start casino`")

        @commands.command()
        async def balance(self, ctx):
            bal = get_balance(ctx.author.id)
            await ctx.send(f"💰 {ctx.author.mention}, your balance is **{bal} coins**.")

        @commands.command()
        async def send(self, ctx, member: discord.Member, amount: int):
            if amount <= 0:
                await ctx.send("❌ Amount must be positive.")
                return
            
            sender_bal = get_balance(ctx.author.id)
            if sender_bal < amount:
                await ctx.send(f"❌ You don’t have enough coins. Your balance is: {sender_bal}")
            
            receiver_bal = get_balance(member.id)
            set_balance(ctx.author.id, sender_bal - amount)
            set_balance(member.id, receiver_bal + amount)
            await ctx.send(f"✅ {ctx.author.mention} sent {amount} coins to {member.mention}.")

        @commands.command()
        @is_admin()
        async def addmoney(self, ctx, member: discord.Member, amount: int):
            if amount <= 0:
                await ctx.send("❌ Amount must be positive.")
                return
async def setup(bot):
    await bot.add_cog(CasinoBalance(bot))