import asyncio
from database.client import supabase_client


async def get_or_create_user(user_id: int) -> dict:
    loop = asyncio.get_event_loop()

    response = await loop.run_in_executor(
        None,
        lambda: supabase_client.table("users").select("*").eq("id", user_id).execute()
    )

    if response.data:
        return response.data[0]  # Если нашли — возвращаем данные юзера

    new_user = await loop.run_in_executor(
        None,
        lambda: supabase_client.table("users").insert({"id": user_id}).execute()
    )
    return new_user.data[0]


async def create_character(user_id: int, name: str, prompt: str) -> dict:
    loop = asyncio.get_event_loop()

    await get_or_create_user(user_id)

    response = await loop.run_in_executor(
        None,
        lambda: supabase_client.table("characters").insert({
            "user_id": user_id,
            "name": name,
            "prompt": prompt
        }).execute()
    )
    return response.data[0]


async def get_last_character_id(user_id: int) -> int | None:
    try:
        response = supabase_client.table("users").select("last_character_id").eq("id", user_id).execute()

        if response.data:
            user_row = response.data[0]
            return user_row.get("last_character_id")

        return None

    except Exception as e:
        print(f"Ошибка при получении ID персонажа для {user_id}: {e}")
        return None


async def get_active_character_name(user_id: int) -> str | None:
    char_id = await get_last_character_id(user_id)
    if not char_id:
        return None

    try:
        response = supabase_client.table("characters").select("name").eq("id", char_id).execute()
        if response.data:
            return response.data[0].get("name")
        return None
    except Exception as e:
        print(f"Ошибка при получении имени персонажа: {e}")
        return None