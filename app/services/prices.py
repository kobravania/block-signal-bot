import httpx
import asyncio

COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"

async def get_price(symbol: str, vs_currency: str = "usd") -> float | None:
    """
    Получить текущую цену монеты с CoinGecko.
    ⚠️ symbol = coingecko-id (например 'bitcoin', 'ethereum', 'dogecoin')
    """
    try:
        params = {"ids": symbol.lower(), "vs_currencies": vs_currency.lower()}
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(COINGECKO_API, params=params)
            r.raise_for_status()
            data = r.json()
        return data.get(symbol.lower(), {}).get(vs_currency.lower())
    except Exception as e:
        print(f"[get_price] Error: {e}")
        return None