import os
import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          ContextTypes, filters, CallbackQueryHandler)

TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
PORT = int(os.getenv("PORT", 8443))

logging.basicConfig(level=logging.INFO)

start_buttons = [
    ["Получить запись эфира 27 апреля 2025 года"],
    ["Записаться на консультацию"],
    ["Задать вопрос или отправить предложение для ablab.pro или Анастасии Бурмистровой"],
    ["Узнать детали PR-обучения"]
]

back_button = [["Вернуться назад"]]

course_buttons = [["Да, пожалуйста"], ["Нет, не актуально"], ["Вернуться назад"]]

main_menu = ReplyKeyboardMarkup(start_buttons, resize_keyboard=True)
back_menu = ReplyKeyboardMarkup(back_button, resize_keyboard=True)
course_menu = ReplyKeyboardMarkup(course_buttons, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Спасибо, что перешли на пиар-бот ablab.pro.\n\nЧто вас интересует?",
        reply_markup=main_menu
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Получить запись эфира 27 апреля 2025 года":
        await update.message.reply_text(
            "Видео доступно для просмотра по ссылке:\nhttps://youtu.be/lxjhYaS1BAo",
            reply_markup=back_menu
        )

    elif text == "Записаться на консультацию":
        await update.message.reply_text(
            "Консультация стоит 30 000 рублей или 300 евро, длится 1-1.5 часа. Подобрать удобный слот можно у @anastasiaboo",
            reply_markup=back_menu
        )

    elif text == "Задать вопрос или отправить предложение для ablab.pro или Анастасии Бурмистровой":
        await update.message.reply_text(
            "Смело направляйте сразу Анастасии @anastasiaboo",
            reply_markup=back_menu
        )

    elif text == "Узнать детали PR-обучения":
        await update.message.reply_text(
            "Прямо сейчас я набираю группу на обновленный расширенный курс по всем инструментам пиара.\n\n"
            "Вот программа:\n\n"
            "БЛОК 1. ОСНОВЫ PR \U0001F4DA\n"
            "01. Что такое PR сегодня: управление репутацией и точками контакта\n"
            "02. Кто такой пиарщик в 2025 году: ключевая функция для роста\n"
            "03. Медиа-чутьё и PR-мышление: инфоповоды и стратегия\n\n"
            "БЛОК 2. ЛИЧНЫЙ БРЕНД \u2728\n"
            "04. Личный бренд: восприятие и репутация\n"
            "05. Архетип, голос и стратегия бренда\n"
            "06. Кейсы PR без шума: практические разборы\n\n"
            "БЛОК 3. ПРИКЛАДНОЙ PR \U0001F6E0\ufe0f\n"
            "07. Как писать тексты, которые формируют образ\n"
            "08. Креатив в PR: нестандартные решения\n"
            "09. Быстрая реакция на повестку\n"
            "10. Интеграция PR в бизнес-стратегию",
            reply_markup=course_menu
        )

    elif text == "Да, пожалуйста":
        await update.message.reply_text(
            "ТАРИФ 1\nДоступ только к программе обучения — 110 000 рублей\n\n"
            "ТАРИФ 2\nДоступ к программе обучения + печатный воркбук + 2 онлайн-мастермайнда — 150 000 рублей\n\n"
            "ТАРИФ 3 — эксклюзив, информация доступна на сайте\n\n"
            "Актуальные скидки и предложения (до 15 мая) доступны тут:\nhttps://prschool.ablab.pro/",
            reply_markup=back_menu
        )

    elif text == "Нет, не актуально" or text == "Вернуться назад":
        await update.message.reply_text(
            "Что вас интересует?",
            reply_markup=main_menu
        )

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Подписка доступна: https://paywall.pw/ordbjzar2xdy"
    )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    await app.initialize()
    await app.run_polling() 


if __name__ == '__main__':
    import asyncio
    asyncio.run(app.run_polling())
