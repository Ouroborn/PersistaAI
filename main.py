import logging
import asyncio
from core.config import BOT_TOKEN, GEMINI_API

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from google import genai


logging.basicConfig(level=logging.INFO)

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