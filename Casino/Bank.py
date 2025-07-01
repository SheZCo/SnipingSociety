import discord 
from discord.ext import commands
import json
import os

BALANCE_FILE = "casino_balances.json"
INITIAL_BALANCE = 1000

def load_data():
    """Load the balances and losses JSON data."""
    if not os.path.isfile(BALANCE_FILE):
        return {}
    with open(BALANCE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}
        
def save_data(data):
    """Save the balances and losses JSON data."""
    with open(BALANCE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_data(user_id):
    """Helper to get a user's data dictionary, with defaults."""
    data = load_data()
    user_str = str(user_id)
    if user_str not in data:
        data[user_str] = {"balance":0, "losses": 0, "wins": 0}
        save_data(data)
    return data[user_str]

def get_balance(user_id):
    return get_user_data(user_id).get("balance", 0)

def set_balance(user_id, amount):
    data = load_data()
    user_str = str(user_id)
    if user_str not in data:
        data[user_str] = {"balance": 0, "losses": 0, "wins": 0}
    else:
        data[user_str]["balance"] = amount
    save_data(data)

def get_loss_count(user_id):
    return get_user_data(user_id).get("losses", 0)

def set_loss_count(user_id, count):
    data = load_data()
    user_str = str(user_id)
    if user_id not in data:
        data[user_str] = {"balance": 0, "losses": count, "wins": 0}
    else:
        data[user_str]["losses"] = count
    save_data(data)

def get_win_count(user_id):
    user_data = get_user_data(user_id)
    return user_data.get("wins", 0)

def set_win_count(user_id, count):
    data = load_data()
    user_str = str(user_id)
    if user_str not in data:
        data[user_str] = {"balance": 0, "losses": 0, "wins": count}
    else:
        data[user_str]["wins"] = count
    save_data(data)

def has_account(user_id):
    return str(user_id) in load_data()

def has_roles(*role_names):
    async def predicate(ctx):
        user_roles = [role.name for role in ctx.author.roles]
        return any(role in user_roles for role in role_names)
    return commands.check(predicate)

def is_admin(): 
    return has_roles('Owner', 'The Boys')

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
            set_loss_count(user_id, 0)
            set_win_count(user_id, 0)
            await ctx.send(f"🎉 {ctx.author.mention}, your casino account is ready! You received {INITIAL_BALANCE} coins.")
        else: 
            await ctx.send("❌ Unknown start option. Try `.start casino`")
    @commands.command()
    async def balance(self, ctx):
        if not has_account(ctx.author.id):
            await ctx.send(f"❌ {ctx.author.mention}, you don't have a casino account yet. Use `.start casino` to create one.")
            return
        bal = get_balance(ctx.author.id)
        wins = get_win_count(ctx.author.id)
        await ctx.send(f"💰 {ctx.author.mention}, your balance is **{bal} coins**.")

    @commands.command()
    async def send(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return
        sender_id = ctx.author.id
        receiver_id = member.id
        sender_bal = get_balance(sender_id)
        if sender_bal < amount:
            await ctx.send(f"❌ You don’t have enough coins. Your balance is: {sender_bal}")
            return
        set_balance(sender_id, sender_bal - amount)
        set_balance(receiver_id, get_balance(receiver_id) + amount)
        await ctx.send(f"✅ {ctx.author.mention} sent {amount} coins to {member.mention}.")

    @commands.command()
    @is_admin()
    async def addmoney(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("❌ Amount must be positive.")
            return  
        set_balance(member.id, get_balance(member.id) + amount)
        await ctx.send(f"✅ Added {amount} coins to {member.mention}'s balance.")

async def setup(bot):
    await bot.add_cog(CasinoBalance(bot))