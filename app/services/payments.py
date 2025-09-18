import httpx
from config import COINBASE_API_KEY, COINBASE_BASE_URL, SUBSCRIPTION_PRICE

headers = {
    "X-CC-Api-Key": COINBASE_API_KEY,
    "X-CC-Version": "2018-03-22",
    "Content-Type": "application/json"
}

async def create_charge(name: str, description: str, price: float, currency="USD"):
    """Создание инвойса в Coinbase Commerce"""
    url = f"{COINBASE_BASE_URL}/charges"
    payload = {
        "name": name,
        "description": description,
        "local_price": {"amount": str(price), "currency": currency},
        "pricing_type": "fixed_price"
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json=payload, timeout=10)
        return r.json()
