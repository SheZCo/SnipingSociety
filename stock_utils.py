import reqs_

async def fetch_stock_price(ticker):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                try:
                    result = data['quoteResponse']['result'][0]
                    price = result.get('regularMarketPrice', 'N/A')
                    symbol = result.get('symbol', ticker.upper())
                    return f"💹 {symbol} – ${price}"
                except (IndexError, KeyError):
                    return "❌ No data found for that ticker."
            else:
                return "❌ Failed to fetch stock data."