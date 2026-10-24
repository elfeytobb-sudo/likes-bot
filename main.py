import telebot, requests, os, time, threading
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home(): return "Romancito NA FIXED"
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000))), daemon=True).start()

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot solo para LAN 🇲🇽\nUsa: /like ID\nEj: /like 18377401856")

@bot.message_handler(commands=['like'])
def like(m):
    try:
        parts = m.text.split()
        # Acepta /like 9729697467 o /like us 18377401856 o /like NA 9729697467
        if len(parts) == 2:
            uid = parts[1]
        elif len(parts) >= 3:
            uid = parts[2]
        else:
            return bot.reply_to(m, "Usa: /like ID")

        # Para LAN siempre mandamos como US, que es como lo detecta Garena
        waiting = bot.reply_to(m, f"Enviando a {uid} en NA...")

        # API ROMANCITO / API REAL - sin bloqueo de canal
        # Esta es la que usa el bot de tu foto que te dio 20 likes reales
        url = f"https://free-fire-likes-api.vercel.app/like?uid={uid}&server_name=US"
        
        r = requests.get(url, timeout=20).json()
        
        # Si dice que debes unirte a canal, usa el backup
        if "anonymouspumptrades" in str(r) or "join" in str(r).lower():
            url2 = f"https://api-likes-freefire-6c5c8e5f2e9d.herokuapp.com/like?uid={uid}&server=us"
            r = requests.get(url2, timeout=20).json()

        bot.send_message(m.chat.id, f"Resultado: {r}\n\nSi dice Likes Added: 20 o 100, ya te llegaron. Revisa el juego en el lobby.")

    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

bot.delete_webhook(drop_pending_updates=True)
time.sleep(2)
bot.infinity_polling(skip_pending=True)
