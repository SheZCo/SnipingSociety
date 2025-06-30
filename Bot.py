# SnipingSociety Pump Token Scanner Bot (Dexscreener Edition)

import reqs_
import main_utils
import stock_utils

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())
bot.remove_command('help')




@bot.command()
async def stock(ctx, ticker: str):
    message = await stock_utils.fetch_stock_price(ticker.upper())
    await ctx.send(message)

    
    
for cmd in [main_utils.purge, main_utils.send_help]:
    bot.add_command(cmd)

@bot.event
async def on_ready():
    print(f'🚀 SnipingSociety Bot is live as {bot.user.name}')

bot.run(TOKEN)