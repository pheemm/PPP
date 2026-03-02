import logging

import requests

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
            InlineKeyboardButton("Узнать погоду", callback_data=data['current']['temperature']),
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Пожалуйста выберите:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    await query.edit_message_text(text=f"Нынешняя температура в Москве: {query.data}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Напишите /start для начала работы бота.")


def main() -> None:
    param = {'key': 'zzbbotd6xlg0go56sl3qyn4vocb4b8z0q1h3mqq5',
             'place_id': 'moscow'}
    url = 'https://www.meteosource.com/api/v1/free/point'

    data = requests.get(url, param).json()


    application = Application.builder().token("8716402003:AAEMQKV0rSgCq5Yv6p8tCyRULu7tfpxokWI").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()