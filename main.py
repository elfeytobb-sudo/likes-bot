import telebot
import requests
import os
import time

TOKEN = os.environ.get("BOT_TOKEN")
API_URL = "https://api-likeee-two.vercel.app/like"
bot = telebot.TeleBot(TOKEN)
REGION_FIJA = "NA"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot solo para LAN 🇲🇽\nUsa: /like ID")

@bot.message_handler(commands=['like'])
def like_cmd(m):
    try:
        parts = m.text.split()
        if len(parts) < 2:
            bot.reply_to(m, "Usa: /like TU_ID")
            return
        uid = parts[1] if len(parts)==2 else parts[2]
        url = f"{API_URL}?uid={uid}&server_name={REGION_FIJA}"
        bot.reply_to(m, f"Enviando a {uid} en {REGION_FIJA}...")
        r = requests.get(url, timeout=15).json()
        bot.reply_to(m, f"Resultado: {r}")
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

print("Borrando webhooks viejos...")
bot.delete_webhook(drop_pending_updates=True)
time.sleep(2)
print("Bot LAN online")
bot.infinity_polling(skip_pending=True, timeout=60)
