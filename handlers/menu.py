from core.lexicon import BotMessages, MenuTexts
from utils.keyboards import get_cancel_kb
from utils.keyboards import get_chat_menu_keyboard, get_main_menu_keyboard
from handlers.states import BotStates, CharacterCreation
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
        await message.answer(BotMessages.ERROR_NO_CHAR)
        return

    await state.set_state(BotStates.chatting)
    await message.answer(
        BotMessages.START_CHAT,
        reply_markup=get_chat_menu_keyboard())


@menu_router.message(BotStates.main_menu, F.text == MenuTexts.CREATE_CHAR)
async def start_character_creation(message: Message, state: FSMContext):
    await state.set_state(CharacterCreation.waiting_for_name)
    await message.answer(
        "<b>Шаг 1:</b> Как будут звать твоего персонажа?\n"
        "<i>Лимит: до 30 символов.</i>",
        reply_markup=get_cancel_kb(),
        parse_mode="HTML"
    )


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