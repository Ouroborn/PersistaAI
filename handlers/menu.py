from core.lexicon import BotMessages, MenuTexts
from handlers.keyboards import get_chat_menu_keyboard, get_main_menu_keyboard
from handlers.states import BotStates
from database.requests import get_or_create_user, get_last_character_id, get_active_character_name

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

menu_router = Router()

@menu_router.message(BotStates.main_menu, F.text == MenuTexts.START_CHAT)
async def process_chat(message: Message, state: FSMContext):
    user_id = message.from_user.id
    last_character_id = await get_last_character_id(user_id)

    if last_character_id is None:
        await message.answer("У вас не выбран активный персонаж. Выберите персонажа")
        return

    await state.set_state(BotStates.chatting)
    await message.answer(
        BotMessages.START_CHAT,
        reply_markup=get_chat_menu_keyboard())

@menu_router.message(BotStates.main_menu, F.text == MenuTexts.SETTINGS)
async def process_settings(message: Message):
    await message.answer(BotMessages.SETTINGS_OPEN)


# /start
@menu_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await get_or_create_user(user_id)
    char_name = await get_active_character_name(user_id)

    welcome = ("Работаем. Добро пожаловать в PersistaAI"
               f"\nТекущий персонаж: {char_name}")

    await state.set_state(BotStates.main_menu)
    await message.answer(
        welcome,
        reply_markup=get_main_menu_keyboard()
    )