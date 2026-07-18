from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.lexicon import MenuTexts, ChatTexts, CreateCharacterTexts
from utils.callbacks import CharacterCB


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

def get_chat_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=ChatTexts.OPEN_CHAR_SETTINGS)
        ],
        [
            KeyboardButton(text=ChatTexts.EXIT_CHAT)
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_create_character_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=CreateCharacterTexts.CANCEL)
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_cancel_kb() -> ReplyKeyboardMarkup:
    """Кнопка отмены, которая висит на протяжении всего создания"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )

def get_skip_kb() -> ReplyKeyboardMarkup:
    """Клавиатура с возможностью пропустить шаг"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⏭ Пропустить")],
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )


def get_confirm_kb() -> ReplyKeyboardMarkup:
    """Клавиатура для финального шага"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Сохранить персонажа")],
            [KeyboardButton(text="❌ Сбросить и отменить")]
        ],
        resize_keyboard=True
    )


def get_characters_kb(characters: list, page: int = 0, per_page: int = 5) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    # Высчитываем индексы для среза списка
    start = page * per_page
    end = start + per_page
    page_chars = characters[start:end]

    # Добавляем кнопки с персонажами
    for char in page_chars:
        builder.button(
            text=char['name'],
            callback_data=CharacterCB(action='select', char_id=char['id'], page=page)
        )
    builder.adjust(1)  # По одной кнопке в ряд

    # Строим кнопки пагинации, если персонажей больше, чем влазит на экран
    nav_buttons = []
    if page > 0:
        nav_buttons.append(builder.button(
            text="⬅️",
            callback_data=CharacterCB(action='list', page=page - 1)
        ))

    if end < len(characters):
        nav_buttons.append(builder.button(
            text="➡️",
            callback_data=CharacterCB(action='list', page=page + 1)
        ))

    # Если добавили стрелочки, выравниваем их в один ряд внизу
    if nav_buttons:
        builder.adjust(1, *([len(nav_buttons)]))  # Сначала по 1 в ряд, последняя строка - по кол-ву кнопок навигации

    return builder.as_markup()