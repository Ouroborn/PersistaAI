from aiogram.fsm.state import StatesGroup, State

class BotStates(StatesGroup):
    main_menu = State()
    creating_character = State()
    chatting = State()

class CharacterCreation(StatesGroup):
    waiting_for_name = State()
    waiting_for_personality = State()
    waiting_for_examples = State()
    waiting_for_greeting = State()
    waiting_for_confirmation = State()