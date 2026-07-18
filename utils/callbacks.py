from aiogram.filters.callback_data import CallbackData

# Фабрика для пагинации и выбора персонажа
class CharacterCB(CallbackData, prefix="char"):
    action: str  # 'list', 'select'
    page: int = 0
    char_id: int = 0  # 0, если просто листаем список

# Фабрика для выбора конкретного чата
class ChatCB(CallbackData, prefix="chat"):
    action: str  # 'new', 'select', 'back_to_chars'
    char_id: int
    chat_id: int = 0