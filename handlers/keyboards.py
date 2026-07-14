from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from core.lexicon import MenuTexts, ChatTexts

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