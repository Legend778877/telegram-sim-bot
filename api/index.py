from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# BOT_TOKEN ko Vercel ke env se lena
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_BASE = "https://simxphantom.vercel.app/api/track?number="
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

@app.post("/")
async def telegram_webhook(request: Request):
    data = await request.json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].strip()

        if text.isdigit() or text.startswith("+"):
            try:
                resp = requests.get(API_BASE + text, timeout=10)
                if resp.status_code == 200:
                    result = resp.json()
                    reply = f"📞 Number: {text}\n\nResult:\n{result}"
                else:
                    reply = "❌ API error."
            except Exception as e:
                reply = f"⚠️ Error: {e}"
        else:
            reply = "❓ Kripya ek valid number bhejein (jaise 03001234567)."

        # Telegram ko reply bhejna
        requests.post(TELEGRAM_URL, json={
            "chat_id": chat_id,
            "text": reply
        })

    return {"ok": True}
