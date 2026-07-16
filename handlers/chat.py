from core.lexicon import ChatTexts, BotMessages
from handlers.keyboards import get_main_menu_keyboard
from handlers.states import BotStates

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

chat_router = Router()

@chat_router.message(BotStates.chatting, F.text == ChatTexts.OPEN_CHAR_SETTINGS)
async def char_settings(message: Message):
    await message.answer(
        BotMessages.CHAR_SETTINGS_OPEN
    )

@chat_router.message(BotStates.chatting, F.text == ChatTexts.EXIT_CHAT)
async def go_to_main_menu(message: Message, state: FSMContext, text):
    await state.set_state(BotStates.main_menu)
    text = 'Возвращение в главное меню'

    await message.answer(
        text,
        reply_markup=get_main_menu_keyboard()
    )