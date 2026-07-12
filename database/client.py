from supabase import create_client, Client
from core.config import SUPABASE_URL, SUPABASE_API

supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_API)