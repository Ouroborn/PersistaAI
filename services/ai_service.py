import json
from google import genai
from google.genai import types
from pydantic import BaseModel

from core.config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


# 1. Описываем жесткую схему, которую ждем от ИИ
class CharacterFields(BaseModel):
    example_dialogue: str
    greeting: str


async def generate_missing_fields(
        name: str,
        personality: str,
        examples: str | None,
        greeting: str | None
) -> tuple[str, str]:
    if examples and greeting:
        return examples, greeting

    prompt = f"""
    Ты — профессиональный сценарист ролевых игр.
    Персонаж:
    Имя: {name}
    Характер: {personality}

    Напиши недостающие данные. 
    ВАЖНО: В репликах и описании действий избегай использования двойных кавычек ("). Используй одинарные (') или русские елочки («»).
    """

    try:
        response = await client.aio.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=CharacterFields,
                temperature=0.7
            )
        )

        data = json.loads(response.text)

        final_examples = examples or data.get("example_dialogue",
                                              f"[Пользователь]: Привет!\n[{name}]: *кивает* Привет.")
        final_greeting = greeting or data.get("greeting", f"*смотрит на тебя* Привет. Я {name}.")

        return final_examples, final_greeting

    except Exception as e:
        print(f"Ошибка Gemini API: {e}")
        fallback_examples = examples or f"Пользователь: Привет!\n{name}: *кивает* Привет, о чем поговорим?"
        fallback_greeting = greeting or f"*смотрит на тебя* Здравствуй. Мое имя — {name}."
        return fallback_examples, fallback_greeting