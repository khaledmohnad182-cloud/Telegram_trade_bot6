from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import datetime
import threading

# ---------------------- التوكن ----------------------
TOKEN = "8356379468:AAGLuUh5BuR7rUOcKLB7tXCVo-dGPxqgd3A"

# ---------------------- قائمة الأزواج الأكثر سيولة ----------------------
major_pairs = [
    "EURUSD", "USDJPY", "GBPUSD", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD",
    "EURJPY", "EURGBP", "EURCHF", "EURAUD", "EURCAD", "EURNZD",
    "GBPJPY", "GBPCHF", "GBPAUD", "GBPCAD", "GBPNZD",
    "AUDJPY", "AUDNZD", "AUDCHF", "AUDCAD",
    "CADJPY", "CADCHF", "NZDJPY", "NZDCHF"
]

# ---------------------- دالة البوت ----------------------
async def signal_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # تحويل الرسالة للحروف الكبيرة وحذف الشرط / والمسافات
    pair = update.message.text.upper().replace("/", "").replace(" ", "")
    hour = datetime.datetime.utcnow().hour

    if pair in major_pairs:
        signal = "⬆️ صعود" if hour % 2 == 0 else "⬇️ هبوط"
        await update.message.reply_text(f"{signal} لمدة 2 دقيقة")
    else:
        # أي نص آخر أو /start
        await update.message.reply_text("أرسل زوج عملات صحيح، مثال: EURUSD")

# ---------------------- إعداد البوت ----------------------
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, signal_bot))  # يلتقط أي رسالة نصية

# ---------------------- تشغيل البوت في خلفية Thread ----------------------
def run_bot():
    app.run_polling()

threading.Thread(target=run_bot).start()

# ---------------------- Flask لتجاوز شرط Render للمنفذ HTTP ----------------------
import os
from flask import Flask

web_app = Flask(__name__)
port = int(os.environ.get("PORT", 4000))

@web_app.route('/')
def home():
    return "Bot is running!"

if __name__ == "__main__":
    web_app.run(host="0.0.0.0", port=port)
