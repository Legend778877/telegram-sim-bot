import requests
from flask import Flask, request

app = Flask(__name__)

# 🔑 Yahan aapka Bot Token fix kar diya gaya hai
TOKEN = "8223005238:AAHPP_UDM2NNI9H6785X9kdAjMB53_tdZ7Q"
URL = f"https://api.telegram.org/bot{TOKEN}/"

# ------------------- Format Function -------------------
def format_response(data_list):
    if not data_list:
        return "❌ No record found."

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
            text = data["message"].get("text", "")

            # Agar /start command aaye
            if text == "/start":
                send_message(chat_id, "👋 Welcome! Send me a number or CNIC.")
                return "ok"

            # Otherwise API call
            api_url = f"https://simxphantom.vercel.app/api/track?number={text}"
            try:
                resp = requests.get(api_url)
                data_list = resp.json()
                reply = format_response(data_list)
            except Exception:
                reply = "⚠️ API error, please try again."

            send_message(chat_id, reply)

        return "ok"
    else:
        return "Bot is running fine!"


if __name__ == "__main__":
    app.run(debug=True)
