import telebot
import requests
from flask import Flask

BOT_TOKEN = "8814140528:AAGA1CvRqWtJbAJD4Gnf-gKYil8AfgCp9FU"
OWNER_ID = 7961534891
OWNER_USERNAME = "@recargasjimenez"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def call_api(region, uid):
    url = f"https://free-fire-like-api.vercel.app/like?uid={uid}&server_name={region}"
    try:
        r = requests.get(url, timeout=15)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def home():
    return "Bot Running"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, f"✅ Bot de @recargasjimenez activo!\nUsa: /like BR 9729697467")

@bot.message_handler(commands=['like'])
def like(m):
    try:
        _, region, uid = m.text.split()
        bot.reply_to(m, f"⏳ Enviando likes a {uid}...")
        res = call_api(region, uid)
        bot.reply_to(m, f"✅ Resultado: {res}")
    except:
        bot.reply_to(m, "Formato: /like BR 9729697467")

bot.infinity_polling()
