import telebot
import requests
import os

TOKEN = os.environ.get("BOT_TOKEN")
API_URL = "https://api-likeee-two.vercel.app/like"

bot = telebot.TeleBot(TOKEN)

# FORZADO A LATINOAMÉRICA NORTE
REGION_FIJA = "NA"  # puedes poner "US" también, es lo mismo para LAN

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot solo para LAN 🇲🇽\nUsa: /like ID\nEjemplo: /like 18377401856")

@bot.message_handler(commands=['like'])
def like_cmd(m):
    try:
        parts = m.text.split()
        if len(parts) == 2:
            uid = parts[1]
        elif len(parts) == 3:
            uid = parts[2]  # si ponen /like NA ID, ignoramos el NA
        else:
            bot.reply_to(m, "Usa: /like TU_ID")
            return

        url = f"{API_URL}?uid={uid}&server_name={REGION_FIJA}"
        bot.reply_to(m, f"Enviando likes a {uid} en {REGION_FIJA}...")
        
        r = requests.get(url, timeout=15).json()
        bot.reply_to(m, f"Resultado: {r}")

    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

print("Bot LAN online")
bot.infinity_polling()
