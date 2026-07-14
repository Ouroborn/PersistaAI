from core.lexicon import ChatTexts, BotMessages
from handlers.keyboards import get_main_menu_keyboard
from handlers.states import BotStates

from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, reply_keyboard_markup
from aiogram.fsm.context import FSMContext

chat_router = Router()

@chat_router.message(BotStates.chatting, F.text == ChatTexts.OPEN_CHAR_SETTINGS)
async def char_settings(message: Message):
    await message.answer(
        BotMessages.CHAR_SETTINGS_OPEN
    )

@chat_router.message(BotStates.chatting, F.text == ChatTexts.EXIT_CHAT)
async def exit_chat(message: Message, state: FSMContext):
    await state.set_state(BotStates.main_menu)

    await message.answer(
        "Возвращение в главное меню",
        reply_markup=get_main_menu_keyboard()
    )