import os
import logging
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from google import genai

from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API = os.getenv("GEMINI_API")

client = genai.Client(api_key=GEMINI_API)


if not BOT_TOKEN or not GEMINI_API:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN or GEMINI_API_KEY in .env file")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Работаем"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())