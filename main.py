import logging

import requests
import httpx

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def fetch_current_temperature(place_id: str) -> float:
    params = {"key": 'zzbbotd6xlg0go56sl3qyn4vocb4b8z0q1h3mqq5', "place_id": 'moscow'}

    timeout = httpx.Timeout(10.0)  # сек
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.get("https://www.meteosource.com/api/v1/free/point", params=params)
        resp.raise_for_status()
        data = resp.json()

    temp = data["current"]["temperature"]

    return temp


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
            [InlineKeyboardButton("Узнать погоду", callback_data=f"weather:{'moscow'}")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Пожалуйста выберите:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    data = query.data or ""
    parts = data.split(":", 1)
    action = parts[0]
    place_id = parts[1] if len(parts) == 2 else 'moscow'

    temp = await fetch_current_temperature(place_id)
    await query.edit_message_text(text=f"Нынешняя температура в Москве: {temp}°C")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Напишите /start для начала работы бота.")


def main() -> None:
    application = Application.builder().token("8716402003:AAEMQKV0rSgCq5Yv6p8tCyRULu7tfpxokWI").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()