import html

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.client import supabase_client
from handlers.chat import go_to_main_menu
from utils.keyboards import get_confirm_kb, get_skip_kb
from handlers.states import CharacterCreation
from services.ai_service import generate_missing_fields

creation_router = Router()

@creation_router.message(CharacterCreation(), F.text.in_({"❌ Отмена", "❌ Сбросить и отменить"}))
async def cancel_creation_handler(message: Message, state: FSMContext):
    await go_to_main_menu(message, state, text="Создание персонажа прервано. Возвращаюсь в главное меню. ↩️")


# ==========================================
#          ПОШАГОВЫЙ СЦЕНАРИЙ FSM
# ==========================================


# Шаг 1: Принимаем ИМЯ ➡️ ждем ХАРАКТЕР
@creation_router.message(CharacterCreation.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    if message.text is None: return  # Защита для PyCharm

    if len(message.text) > 30:
        await message.answer(f"⚠️ Имя слишком длинное ({len(message.text)}/30 симв.)")
        return

    await state.update_data(name=message.text)
    await state.set_state(CharacterCreation.waiting_for_personality)
    await message.answer(
        f"Имя: <b>{message.text}</b>!\n\n"
        f"<b>Шаг 2:</b> Опиши характер, бэкграунд и роль персонажа.\n"
        f"Кто он? Каковы его цели или скрытые страхи?\n"
        f"<i>Лимит: до 600 символов.</i>",
        parse_mode="HTML"
    )


# Шаг 2: Принимаем ХАРАКТЕР ➡️ ждем ПРИМЕРЫ ДИАЛОГОВ
@creation_router.message(CharacterCreation.waiting_for_personality)
async def process_personality(message: Message, state: FSMContext):
    if message.text is None: return

    if len(message.text) > 600:
        await message.answer(f"⚠️ Описание слишком раздуто ({len(message.text)}/600 симв.)")
        return

    await state.update_data(personality=message.text)
    await state.set_state(CharacterCreation.waiting_for_examples)
    await message.answer(
        "Характер зафиксирован! 🧠\n\n"
        "<b>Шаг 3:</b> Пришли примеры реплик, чтобы задать манеру речи.\n"
        "<i>Или нажми кнопку ниже, чтобы ИИ придумал их сам</i>",
        # Меняем клавиатуру на клавиатуру с пропуском
        reply_markup=get_skip_kb(),
        parse_mode="HTML"
    )

# Шаг 3: Принимаем ПРИМЕРЫ ➡️ ждем ПРИВЕТСТВИЕ
@creation_router.message(CharacterCreation.waiting_for_examples)
async def process_examples(message: Message, state: FSMContext):
    if message.text is None: return

    # Если пропустили — пишем в базу None, иначе — текст пользователя
    if message.text == "⏭ Пропустить":
        await state.update_data(examples=None)
    else:
        await state.update_data(examples=message.text)

    await state.set_state(CharacterCreation.waiting_for_greeting)
    await message.answer(
        "Принято! 💬\n\n"
        "<b>Шаг 4:</b> Напиши приветственную фразой персонажа.\n"
        "<i>Или нажми кнопку ниже, чтобы доверить это ИИ!</i>",
        reply_markup=get_skip_kb(),
        parse_mode="HTML"
    )


# Шаг 4: Принимаем ПРИВЕТСТВИЕ ➡️ Автогенерация пропущенного ➡️ Превью
@creation_router.message(CharacterCreation.waiting_for_greeting)
async def process_greeting(message: Message, state: FSMContext):
    if message.text is None: return

    if message.text != "⏭ Пропустить":
        if len(message.text) > 400:
            await message.answer(f"⚠️ Приветствие слишком длинное ({len(message.text)}/400 симв.).")
            return
        await state.update_data(greeting=message.text)
    else:
        await state.update_data(greeting=None)

    # Вытаскиваем текущие данные
    user_data = await state.get_data()
    name = user_data["name"]
    personality = user_data["personality"]
    examples = user_data.get("examples")
    greeting = user_data.get("greeting")

    # Если хоть одно поле пропущено — показываем юзеру, что ИИ начал думать
    if examples is None or greeting is None:
        waiting_msg = await message.answer(
            "🪄 <i>ИИ анализирует характер и придумывает недостающие детали... Подожди секунду...</i>",
            parse_mode="HTML")

        # Здесь мы вызываем твою функцию генерации через Gemini
        # Допустим, она возвращает кортеж (generated_examples, generated_greeting)
        gen_examples, gen_greeting = await generate_missing_fields(name, personality, examples, greeting)

        # Записываем сгенерированное в state
        await state.update_data(examples=gen_examples, greeting=gen_greeting)
        user_data = await state.get_data()  # Обновляем локальные данные для превью

        # Удаляем временную плашку "ИИ думает"
        await waiting_msg.delete()

    # ЭКРАНИРУЕМ ВСЕ ДАННЫЕ ПЕРЕД ВЫВОДОМ
    safe_name = html.escape(user_data['name'])
    safe_personality = html.escape(user_data['personality'])
    # Защита от None на случай, если примеры/приветствие не сгенерировались
    safe_examples = html.escape(user_data.get('examples') or '')
    safe_greeting = html.escape(user_data.get('greeting') or '')

    # Показываем красивое превью (в котором уже точно всё заполнено!)
    preview_text = (
        "==<b>ПРЕВЬЮ ПЕРСОНАЖА</b>==\n\n"
        f"👤 <b>Имя:</b> {safe_name}\n"
        f"📝 <b>Характер:</b> {safe_personality}\n\n"
        f"💬 <b>Примеры общения:</b>\n<code>{safe_examples}</code>\n\n"
        f"👋 <b>Приветствие:</b> <i>{safe_greeting}</i>\n\n"
        "Все верно? Подтверди сохранение персонажа."
    )

    await state.set_state(CharacterCreation.waiting_for_confirmation)
    await message.answer(preview_text, reply_markup=get_confirm_kb(), parse_mode="HTML")


# Шаг 5: ПОДТВЕРЖДЕНИЕ ➡️ Запись в Supabase
@creation_router.message(CharacterCreation.waiting_for_confirmation, F.text == "✅ Сохранить персонажа")
async def process_confirmation(message: Message, state: FSMContext):
    if message.from_user is None: return  # Снова type guard

    user_data = await state.get_data()

    try:
        payload = {
            "user_id": message.from_user.id,
            "name": user_data["name"],
            "personality": user_data["personality"],
            "example_dialogue": user_data["examples"],
            "greeting": user_data["greeting"]
        }

        supabase_client.table("characters").insert(payload).execute()

        await go_to_main_menu(
            message,
            state,
            text=f"Персонаж <b>{user_data['name']}</b> успешно создан и сохранен."
        )

    except Exception as e:
        await go_to_main_menu(
            message,
            state,
            text=f"❌ Ошибка при сохранении в базу данных. Попробуй позже.\nЛог: {e}"
        )