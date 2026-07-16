from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from core.lexicon import MenuTexts, ChatTexts, CreateCharacterTexts


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