import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API = os.getenv("GEMINI_API")
SUPABASE_API = os.getenv("SUPABASE_API")
SUPABASE_URL = os.getenv("SUPABASE_URL")