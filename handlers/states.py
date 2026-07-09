from aiogram.fsm.state import StatesGroup, State

class BotStates(StatesGroup):
    main_menu = State()
    creating_character = State()
    chatting = State()