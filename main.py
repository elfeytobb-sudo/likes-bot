import telebot
import requests
import os

# --- CONFIG ---
TOKEN = os.environ.get("BOT_TOKEN")  # En Render pon tu token en Environment -> BOT_TOKEN
# Si lo pruebas en tu PC, puedes ponerlo directo aquí: TOKEN = "123456:ABC..."
API_URL = "https://api-likeee-two.vercel.app/like"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(m):
    msg = (
        "🔥 *Bot de Romancito - 300 Likes BR* 🔥\n\n"
        "Usa el comando:\n"
        "`/like BR TU_ID`\n\n"
        "Ejemplo:\n"
        "`/like BR 9729697467`"
    )
    bot.reply_to(m, msg, parse_mode="Markdown")

@bot.message_handler(commands=['like'])
def like_cmd(m):
    try:
        parts = m.text.split()
        if len(parts) < 3:
            bot.reply_to(m, "❌ *Formato incorrecto*\nUsa: `/like BR 9729697467`", parse_mode="Markdown")
            return
        
        region = parts[1].upper()
        uid = parts[2]

        sent = bot.reply_to(m, f"⏳ *Enviando 300 likes a {uid} en {region}...*", parse_mode="Markdown")

        url = f"{API_URL}?uid={uid}&server_name={region}"
        r = requests.get(url, timeout=20).json()

        if r.get("status") == 1 or r.get("likes"):
            texto = (
                f"✅ *¡300 Likes Enviados con Éxito!*\n\n"
                f"🆔 *UID:* `{uid}`\n"
                f"🌎 *Región:* {region}\n"
                f"❤️ *Likes:* {r.get('likes', 300)}\n"
                f"📡 *Server:* {r.get('server', region)}\n\n"
                f"_Bot de Romancito 🇩🇴_"
            )
            bot.edit_message_text(texto, chat_id=m.chat.id, message_id=sent.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text(f"❌ *Error:* No se pudo enviar likes a {uid}\n`{r}`", chat_id=m.chat.id, message_id=sent.message_id, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(m, f"❌ Error: {e}")

print("Bot ONLINE - BR 300 Likes")
bot.infinity_polling()
    
