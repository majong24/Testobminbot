import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

keyboard = ReplyKeyboardMarkup(
    [["Опублікувати курс"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Натисни «Опублікувати курс» і відправ курси так:\n\n"
        "USD 44.80 45.10\n"
        "EUR 52.10 52.35\n"
        "GBP 59.10 59.80\n"
        "CHF 56.50 57.20\n"
        "PLN 12.20 12.30\n"
        "CZK 2.00 2.10",
        reply_markup=keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Опублікувати курс":
        await update.message.reply_text(
            "Відправ курси одним повідомленням:\n\n"
            "USD 44.80 45.10\n"
            "EUR 52.10 52.35\n"
            "GBP 59.10 59.80\n"
            "CHF 56.50 57.20\n"
            "PLN 12.20 12.30\n"
            "CZK 2.00 2.10"
        )
        return

    now = datetime.now()
    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%H:%M")

    post = f"""💱 ОБМІН ВАЛЮТ | ПОЛТАВА

📅 Сьогодні: {date}
🕘 Актуальний курс на {time}

🇺🇸 USD-UAH 🇺🇦 {get_rate(text, "USD")}
🇪🇺 EUR-UAH 🇺🇦 {get_rate(text, "EUR")}
🇬🇧 GBP-UAH 🇺🇦 {get_rate(text, "GBP")}
🇨🇭 CHF-UAH 🇺🇦 {get_rate(text, "CHF")}
🇵🇱 PLN-UAH 🇺🇦 {get_rate(text, "PLN")}
🇨🇿 CZK-UAH 🇺🇦 {get_rate(text, "CZK")}

☎️ Оптовий курс за дзвінком

♻️ Коригування курсу протягом дня 🔄

📍 Ми знаходимось:
м. Полтава, вул. Соборності 76-77
зупинка Зигіна, зі сторони ТРЦ Київ

⏰ Графік роботи:
Без вихідних з 8:00 до 19:00

☎️ Наш контакт:
+380 (68) 156 63 38
"""

    await context.bot.send_message(chat_id=CHANNEL_ID, text=post)
    await update.message.reply_text("✅ Курс опубліковано в канал!")

def get_rate(text, currency):
    for line in text.splitlines():
        if line.upper().startswith(currency):
            parts = line.split()
            if len(parts) >= 3:
                return f"{parts[1]}–{parts[2]}"
    return "—"

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот обменника запущен")
    app.run_polling()

if __name__ == "__main__":
    main()
