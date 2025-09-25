import requests
from flask import Flask, request

app = Flask(__name__)

# 🔑 Aapka Bot Token (already added)
TOKEN = "8223005238:AAGVt3huiJNqiRcs9G9nv2QwWUNk8QGe78w"
URL = f"https://api.telegram.org/bot{TOKEN}/"


# ------------------- Format Function -------------------
def format_response(data_list):
    if not data_list:
        return "❌ This number data not received."

    header = "🎯 INFO RECEIVED\n✅ Status: Successful\n\n"
    formatted = [header]

    for item in data_list:
        block = (
            "━━━━━━━━━━━━━━━\n"
            f"👤 Name: {item.get('Name','N/A')}\n"
            f"📱 Mobile: {item.get('Mobile','N/A')}\n"
            f"🪪 CNIC: {item.get('CNIC','N/A')}\n"
            f"🏠 Address: {item.get('Address','N/A')}\n"
            f"🌍 Country: {item.get('Country','N/A')}\n"
        )
        formatted.append(block)

    formatted.append("━━━━━━━━━━━━━━━")
    return "\n".join(formatted)


# ------------------- Send Message -------------------
def send_message(chat_id, text):
    url = URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)


# ------------------- Webhook Route -------------------
@app.route("/", methods=["POST", "GET"])
def webhook():
    if request.method == "POST":
        data = request.get_json()
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "").strip()

            # 📌 Commands handle
            if text == "/start":
                send_message(chat_id, "👋 Welcome! Send me a number or CNIC to get details.")
                return "ok"

            if text == "/help":
                help_text = (
                    "📖 *Help Menu*\n\n"
                    "➡️ Send me any mobile number or CNIC, I will fetch data for you.\n"
                    "➡️ Use /about to know about this bot.\n"
                )
                send_message(chat_id, help_text)
                return "ok"

            if text == "/about":
                about_text = (
                    "🤖 *About This Bot*\n\n"
                    "This bot is created for educational demo.\n"
                    "It fetches SIM & CNIC info using API.\n"
                )
                send_message(chat_id, about_text)
                return "ok"

            # 📌 Otherwise API call
            api_url = f"https://simxphantom.vercel.app/api/track?number={text}"
            try:
                resp = requests.get(api_url)
                data_list = resp.json()
                reply = format_response(data_list)
            except Exception:
                reply = "❌ This number data not received."

            send_message(chat_id, reply)

        return "ok"
    else:
        return "Bot is running fine!"


if __name__ == "__main__":
    app.run(debug=True)
