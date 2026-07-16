# services/ai_service.py
import json
from google import genai
from google.genai import types
from core.config import GEMINI_API_KEY

# Инициализируем клиент.
# Он автоматически подтянет ключ из переменной окружения GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)


async def generate_missing_fields(
        name: str,
        personality: str,
        examples: str | None,
        greeting: str | None
) -> tuple[str, str]:
    """
    Асинхронно генерирует примеры диалога и/или приветствие через Gemini.
    """
    if examples and greeting:
        return examples, greeting

    prompt = f"""
    Ты — профессиональный геймдизайнер, сценарист и эксперт по ролевым играм.
    У нас есть персонаж:
    Имя: {name}
    Характер и описание: {personality}

    Твоя задача — дописать недостающие поля для карточки персонажа.
    """

    if not examples:
        prompt += "\nСгенерируй пример диалога (поле example_dialogue) в формате Few-Shot (диалог из 2-3 реплик с действиями в звездочках *...*)."
    if not greeting:
        prompt += "\nСгенерируй приветствие (поле greeting) — первую фразу при встрече, отражающую характер, с действиями в звездочках *...*."

    prompt += """
    Верни строго JSON-формат (без Markdown-разметки типа ```json):
    {
      "example_dialogue": "текст примеров диалога",
      "greeting": "текст приветствия"
    }
    Если какое-то поле уже было передано (не равно null), верни его без изменений.
    """

    try:
        response = await client.aio.models.generate_content(
            model='gemini-1.5-flash',  # <-- Меняем на более стабильную 1.5-flash
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )

        data = json.loads(response.text)

        # Заменяем <user> на [Пользователь], чтобы избежать конфликтов с HTML парсером
        final_examples = examples or data.get("example_dialogue",
                                              f"[Пользователь]: Привет!\n[Персонаж]: *кивает* Привет. Я {name}.")
        final_greeting = greeting or data.get("greeting", f"*смотрит на тебя* Привет. Я {name}. Чего ты хочешь?")

        return final_examples, final_greeting

    except Exception as e:
        print(f"Ошибка Gemini API: {e}")
        # Безопасный резервный вариант без треугольных скобок
        fallback_examples = examples or f"Пользователь: Привет!\n{name}: *спокойно кивает* Привет, я {name}. О чем ты хотел поговорить?"
        fallback_greeting = greeting or f"*смотрит на тебя в упор* Здравствуй. Мое имя — {name}."
        return fallback_examples, fallback_greeting