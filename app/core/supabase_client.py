from supabase import create_client, Client
from app.core.config import config

def get_supabase() -> Client:
    return create_client(config.supabase_url, config.supabase_key)