import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (ApplicationBuilder, CommandHandler, CallbackQueryHandler,
                          ContextTypes, MessageHandler, filters)

BOT_TOKEN = os.getenv("BOT_TOKEN")
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
PORT = int(os.getenv("PORT", "8443"))

if not BOT_TOKEN or not RENDER_EXTERNAL_HOSTNAME:
    raise ValueError("Missing environment variables BOT_TOKEN or RENDER_EXTERNAL_HOSTNAME")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Получить запись эфира 27 апреля 2025 года", callback_data="option_1")],
        [InlineKeyboardButton("Записаться на консультацию", callback_data="option_2")],
        [InlineKeyboardButton("Задать вопрос или отправить предложение", callback_data="option_3")],
        [InlineKeyboardButton("Узнать детали PR-обучения", callback_data="option_4")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет! Спасибо, что перешли на пиар-бот ablab.pro.\n\nЧто вас интересует?",
        reply_markup=reply_markup
    )

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "option_1":
        await query.edit_message_text("Видео доступно для просмотра по ссылке:\nhttps://youtu.be/lxjhYaS1BAo", reply_markup=back_button())

    elif query.data == "option_2":
        await query.edit_message_text("Консультация стоит 30 000 рублей или 300 евро, длится 1-1.5 часа. Подобрать удобный слот можно у @anastasiaboo", reply_markup=back_button())

    elif query.data == "option_3":
        await query.edit_message_text("Смело направляйте сразу Анастасии @anastasiaboo", reply_markup=back_button())

    elif query.data == "option_4":
        keyboard = [[InlineKeyboardButton("Прислать условия?", callback_data="option_4_details")]]
        await query.edit_message_text(
            "Прямо сейчас я набираю группу на обновленный расширенный курс по всем инструментам пиара.\n\n"
            "Вот программа: \n\n"
            "БЛОК 1. ОСНОВЫ PR \ud83d\udcda\n"
            "01. Что такое PR сегодня: управление репутацией и точками контакта\n"
            "02. Кто такой пиарщик в 2025 году: ключевая функция для роста\n"
            "03. Медиа-чутьё и PR-мышление: инфоповоды и стратегия\n\n"
            "БЛОК 2. ЛИЧНЫЙ БРЕНД \u2728\n"
            "04. Личный бренд: восприятие и репутация\n"
            "05. Архетип, голос и стратегия бренда\n"
            "06. Кейсы PR без шума: практические разборы\n\n"
            "БЛОК 3. ПРИКЛАДНОЙ PR \ud83d\udee0\ufe0f\n"
            "07. Как писать тексты, которые формируют образ\n"
            "08. Креатив в PR: нестандартные решения\n"
            "09. Быстрая реакция на повестку\n"
            "10. Интеграция PR в бизнес-стратегию",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "option_4_details":
        keyboard = [
            [InlineKeyboardButton("Да, пожалуйста", callback_data="tariffs")],
            [InlineKeyboardButton("Нет, не актуально", callback_data="back")]
        ]
        await query.edit_message_text("Прислать условия?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "tariffs":
        await query.edit_message_text(
            "ТАРИФ 1\nДоступ только к программе обучения — 110 000 рублей\n\n"
            "ТАРИФ 2\nДоступ к программе обучения + печатный воркбук + 2 онлайн-мастермайнда — 150 000 рублей\n\n"
            "ТАРИФ 3 — эксклюзив, информация доступна на сайте\n\n"
            "Актуальные скидки и предложения (до 15 мая) доступны тут:\nhttps://prschool.ablab.pro/",
            reply_markup=back_button()
        )

    elif query.data == "back":
        await start(update, context)


def back_button():
    return InlineKeyboardMarkup([[InlineKeyboardButton("◀ Вернуться назад", callback_data="back")]])

async def access_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Подписка доступна https://paywall.pw/ordbjzar2xdy")

async def set_commands(app):
    commands = [
        BotCommand("start", "Перезапустить бот"),
        BotCommand("subscribe", "Получить доступ в закрытый канал")
    ]
    await app.bot.set_my_commands(commands)

if __name__ == "__main__":
    async def main():
        app = ApplicationBuilder().token(BOT_TOKEN).build()

        await set_commands(app)

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("subscribe", access_channel))
        app.add_handler(CallbackQueryHandler(handle_menu))

        await app.bot.set_webhook(
            url=f"https://{RENDER_EXTERNAL_HOSTNAME}/telegram",
            drop_pending_updates=True
        )
        await app.start()
        await app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_path="/telegram"
        )

    import asyncio
    asyncio.run(main())
