from core.lexicon import BotMessages, MenuTexts
from handlers.states import BotStates

from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

menu_router = Router()

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=MenuTexts.START_CHAT),
            KeyboardButton(text=MenuTexts.CHANGE_CHAR)
        ],
        [
            KeyboardButton(text=MenuTexts.CREATE_CHAR),
            KeyboardButton(text=MenuTexts.SETTINGS)
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

@menu_router.message(BotStates.main_menu, F.text == MenuTexts.SETTINGS)
async def process_settings(message: Message):
    await message.answer(BotMessages.SETTINGS_OPEN)


# /start
@menu_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(BotStates.main_menu)

    await message.answer(
        BotMessages.WELCOME,
        reply_markup=get_main_menu_keyboard()
    )