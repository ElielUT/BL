from supabase import create_client, Client
from app.core.config import config
from sqlalchemy.orm import declarative_base

def get_supabase() -> Client:
    return create_client(config.supabase_url, config.supabase_key)

Base = declarative_base()

def get_db():
    # Placeholder for database session. 
    # Proper implementation requires DATABASE_URL in config/env.
    yield None