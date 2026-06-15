from datetime import datetime, time
from zoneinfo import ZoneInfo
import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

rates = {
    "USD": ("44.80", "45.10"),
    "EUR": ("52.10", "52.35"),
    "GBP": ("59.10", "59.80"),
    "CHF": ("56.50", "57.20"),
    "PLN": ("12.20", "12.30"),
    "CZK": ("2.00", "2.10"),
}

flags = {
    "USD": "🇺🇸",
    "EUR": "🇪🇺",
    "GBP": "🇬🇧",
    "CHF": "🇨🇭",
    "PLN": "🇵🇱",
    "CZK": "🇨🇿",
}

waiting_currency = {}

def main_keyboard():
    return ReplyKeyboardMarkup(
        [["✏️ Редагувати курс"], ["📢 Опублікувати курс"]],
        resize_keyboard=True
    )

def currency_keyboard():
    return ReplyKeyboardMarkup(
        [
            [f"🇺🇸 USD {rates['USD'][0]}–{rates['USD'][1]}", f"🇪🇺 EUR {rates['EUR'][0]}–{rates['EUR'][1]}"],
            [f"🇬🇧 GBP {rates['GBP'][0]}–{rates['GBP'][1]}", f"🇨🇭 CHF {rates['CHF'][0]}–{rates['CHF'][1]}"],
            [f"🇵🇱 PLN {rates['PLN'][0]}–{rates['PLN'][1]}", f"🇨🇿 CZK {rates['CZK'][0]}–{rates['CZK'][1]}"],
            ["📢 Опублікувати курс"],
        ],
        resize_keyboard=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привіт! Тут можна редагувати курс валют і публікувати його в канал.",
        reply_markup=main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if text == "✏️ Редагувати курс":
        await update.message.reply_text(
            "Оберіть валюту, яку хочете змінити:",
            reply_markup=currency_keyboard()
        )
        return

    if text == "📢 Опублікувати курс":
        await publish_course(update, context)
        return

    selected = None
    for cur in rates.keys():
        if cur in text:
            selected = cur
            break

    if selected:
        waiting_currency[user_id] = selected
        await update.message.reply_text(
            f"Введіть новий курс {selected} у форматі:\n\n"
            f"{rates[selected][0]} {rates[selected][1]}"
        )
        return

    if user_id in waiting_currency:
        cur = waiting_currency[user_id]
        parts = text.replace(",", ".").split()

        if len(parts) != 2:
            await update.message.reply_text("❌ Введіть два числа, наприклад: 44.80 45.10")
            return

        rates[cur] = (parts[0], parts[1])
        waiting_currency.pop(user_id)

        await update.message.reply_text(
            f"✅ {cur} оновлено: {parts[0]}–{parts[1]}\n\n"
            "Оберіть наступну валюту або натисніть «📢 Опублікувати курс».",
            reply_markup=currency_keyboard()
        )
        return

    await update.message.reply_text(
        "Натисніть «✏️ Редагувати курс» або «📢 Опублікувати курс».",
        reply_markup=main_keyboard()
    )

async def publish_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now()
    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%H:%M")

    post = f"""💱 ОБМІН ВАЛЮТ | ПОЛТАВА

📅 Сьогодні: {date}
🕘 Актуальний курс на {time}

🇺🇸 USD-UAH 🇺🇦 {rates['USD'][0]}–{rates['USD'][1]}
🇪🇺 EUR-UAH 🇺🇦 {rates['EUR'][0]}–{rates['EUR'][1]}
🇬🇧 GBP-UAH 🇺🇦 {rates['GBP'][0]}–{rates['GBP'][1]}
🇨🇭 CHF-UAH 🇺🇦 {rates['CHF'][0]}–{rates['CHF'][1]}
🇵🇱 PLN-UAH 🇺🇦 {rates['PLN'][0]}–{rates['PLN'][1]}
🇨🇿 CZK-UAH 🇺🇦 {rates['CZK'][0]}–{rates['CZK'][1]}

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
    await update.message.reply_text("✅ Курс опубліковано в канал!", reply_markup=main_keyboard())

async def auto_publish(context):
    with open("6BCDAD66-6AD8-4EEF-A5E7-3629C0D5A573.png", "rb") as photo:
        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            caption="💱 Актуальний курс валют"
        )
        async def main():    
        app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.job_queue.run_daily(
    auto_publish,
    time=time(hour=8, minute=0, tzinfo=ZoneInfo("Europe/Kyiv"))
)

    print("Бот обменника запущен")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    import asyncio
    await asyncio.Event().wait()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
