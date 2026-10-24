import telebot
import requests
import os
from flask import Flask
from threading import Thread

BOT_TOKEN = "8814140528:AAGA1CvRqWtJbAJD4Gnf-gKYil8AfgCp9FU"
OWNER_ID = 7961534891
OWNER_USERNAME = "@recargasjimenez"
bot = telebot.TeleBot(BOT_TOKEN)

# --- Mantiene vivo Render ---
app = Flask('')
@app.route('/')
def home():
    return "Bot de @recargasjimenez Activo!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- API de Likes ---
def call_api(region, uid):
    url = f"https://free-fire-like-api.vercel.app/like?uid={uid}&server_name={region}"
    try:
        r = requests.get(url, timeout=20)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# --- Comandos ---
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🔥 Bot de @recargasjimenez Online!\n\nUso:\n/like BR 9729697467\nEjemplo:\n/like BR 1234567890")

@bot.message_handler(commands=['like'])
def like_cmd(m):
    try:
        parts = m.text.split()
        if len(parts) < 3:
            bot.reply_to(m, "Formato: /like REGION ID\nEj: /like BR 9729697467")
            return
        region = parts[1].upper()
        uid = parts[2]
        
        bot.reply_to(m, f"⏳ Enviando likes a {uid} en {region}
