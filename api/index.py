import os
import requests
from flask import Flask, request

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].strip()

        if text.replace("+", "").isdigit():
            api_url = f"https://simxphantom.vercel.app/api/track?number={text}"
            try:
                resp = requests.get(api_url)
                reply = resp.text
            except Exception:
                reply = "API error, please try again."

            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                          json={"chat_id": chat_id, "text": reply})
    return "ok"
