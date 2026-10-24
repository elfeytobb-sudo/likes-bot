import os
import telebot
import requests
from flask import Flask
import threading

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_URL = "https://api-likee.vercel.app/like"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot running!"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Hola! Usa: /like BR 9729697467")

@bot.message_handler(commands=['like'])
def like_cmd(m):
    try:
        parts = m.text.split()
        if len(parts) < 3:
            bot.reply_to(m, "Formato: /like BR 9729697467")
            return
        _, region, uid = parts
        bot.reply_to(m, f"Enviando likes a {uid}...")
        # Nueva API usa uid y server_name
        r = requests.get(f"{API_URL}?uid={uid}&server_name={region}")
        bot.reply_to(m, f"Resultado: {r.text[:1000]}")
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
