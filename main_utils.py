import reqs_

async def send_help(ctx, topic: str=None):
    if topic is None: 
        embed = discord.Embed(
            title="🛡️ SnipingSociety Bot Help",
            description="Type `.help [category]` to view commands in that area.",
            color=discord.Color.dark_purple()
        )
        embed.add_field(name="📈 .help stocks", value="Commands for sniping stocks/options.", inline=False)
        embed.add_field(name="p💰 .help crypto", value="Crypto, sniping, flipping tools.", inline=False)
        embed.add_field(name="🏹 .ping", value="Check if the bot is online and ready.", inline=False)
        embed.add_field(name="🧹 .purge", value="Clear messages in a channel.", inline=False)
        embed.set_footer(text="SnipingSociety | Stay sharp, stay profitable ⚡")
        await ctx.send(embed=embed)
        
    elif topic.lower() == "stocks":
        embed = discord.Embed(
            title="📈 Stock Sniping Commands",
            description="Commands related to stocks, options, and market analysis.",
            color=discord.Color.blue()
        )
        embed.add_field(name="🔎 .stock {ticker}", value="Get live stock data from major exchanges.", inline=False)
        embed.add_field(name="📰 .news {ticker}", value="Pull recent news headlines for a stock.", inline=False)
        embed.add_field(name="📊 .chart {ticker}", value="Send a snapshot chart of the stock price.", inline=False)
        embed.add_field(name="💡 More coming soon!", value="Stay tuned for more pro-level sniper tools.", inline=False)
        embed.set_footer(text="SnipingSociety | Stock Sniping Set")
        await ctx.send(embed=embed)
    elif topic.lower() == "crypto":
        embed = discord.Embed(
            title="💰 Crypto Sniper Commands",
            description="Everything you need to catch pumpers, avoid rugs, and flip fast.",
            color=discord.Color.gold()
        )
        embed.add_field(name="🔫 .snipe dex {ca}", value="Fetch token info from Dexscreener by contract address.", inline=False)
        embed.add_field(name="💎 .gems", value="Get a list of trending tokens and sniper-worthy plays (future).", inline=False)
        embed.add_field(name="💡 More coming soon!", value="Stay tuned for more pro-level sniper tools.", inline=False)
        embed.set_footer(text="SnipingSociety | Crypto Command Set")
        await ctx.send(embed=embed)
        
@commands.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    """Delete the specified number of messages in the channel."""
    if amount < 1 or amount > 100:
        await ctx.send("❌ Please provide a number between 1 and 100.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
    confirm = await ctx.send(f"🧹 Purged {len(deleted)-1} messages!")
    await confirm.delete(delay=5)  # Clean confirmation after 5 seconds
    
async def ping(ctx):
    await ctx.send('🏹 Sniper Ready – Ping Confirmed')