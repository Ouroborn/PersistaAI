import logging
import asyncio
from core.config import BOT_TOKEN, GEMINI_API

from aiogram import Bot, Dispatcher, F
from handlers.menu import menu_router


from google import genai


logging.basicConfig(level=logging.INFO)

client = genai.Client(api_key=GEMINI_API)

if not BOT_TOKEN or not GEMINI_API:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or GEMINI_API_KEY in .env file")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(menu_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())