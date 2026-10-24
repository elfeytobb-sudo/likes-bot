import telebot
import requests
import os

TOKEN = os.environ.get("BOT_TOKEN")
API_URL = "https://api-likeee-two.vercel.app/like"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot online! Usa: /like BR ID o /like NA ID")

@bot.message_handler(commands=['like'])
def like_cmd(m):
    try:
        _, region, uid = m.text.split()
        url = f"{API_URL}?uid={uid}&server_name={region}"
        r = requests.get(url, timeout=15).json()
        bot.reply_to(m, f"Resultado: {r}")
    except Exception as e:
        bot.reply_to(m, f"Error: {e} - Usa: /like BR 123456")

print("Bot online")
bot.infinity_polling()
