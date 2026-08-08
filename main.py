import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder

# خادم ويب بسيط ليبقي البوت مستيقظاً
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# تشغيل البوت
def run_bot():
    TOKEN = os.environ.get("BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()
    # هنا تضع أوامر البوت الخاصة بك
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    threading.Thread(target=run_web_server).start()
    run_bot()
    
