import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")