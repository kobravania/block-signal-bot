from fastapi import FastAPI, Request, Header, HTTPException
import hmac, hashlib
from config import COINBASE_WEBHOOK_SECRET
from models import activate_pro

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request, x_cc_webhook_signature: str = Header(None)):
    body = await request.body()

    signature = hmac.new(
        COINBASE_WEBHOOK_SECRET.encode("utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()

    if signature != x_cc_webhook_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")

    event = await request.json()

    if event["event"]["type"] == "charge:confirmed":
        # допустим, ты хранишь tg_id в "metadata"
        tg_id = event["event"]["data"].get("metadata", {}).get("tg_id")
        if tg_id:
            activate_pro(int(tg_id))
            print(f"✅ Подписка активирована для {tg_id}")

    return {"status": "ok"}
