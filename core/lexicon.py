from database.requests import get_active_character_name

class MenuTexts:
    START_CHAT = "🤖 Начать чат"
    CHANGE_CHAR = "👥 Сменить персонажа"
    CREATE_CHAR = "➕ Создать персонажа"
    SETTINGS = "⚙️ Настройки"

class BotMessages:
    SETTINGS_OPEN = "Настройки:"
    AI_THINKING = "⏳ Персонаж печатает сообщение..."
    ERROR_NO_CHAR = "⚠️ Вы еще не выбрали персонажа!"
    CREATE_CHOOSE_NAME = "Имя:"
    CREATE_CHOOSE_PROMPT = "Системный промпт:"
    CREATE_SUCCESS = "Персонаж создан"
    CANCELED = "Действие отменено"
    CHOOSE_CHAR = "Выберите персонажа"
    START_CHAT = "Чат начат. Напишите свое первое сообщение"
    CHAR_SETTINGS_OPEN = "Настройки персонажа"

class ChatTexts:
    EXIT_CHAT = "Выход"
    OPEN_CHAR_SETTINGS = "Настройки персонажа"