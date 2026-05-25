#FastAPI y Supabase
from fastapi import APIRouter, Path, HTTPException
from app.core.supabase_client import get_supabase
from app.core.config import config

router = APIRouter()

@router.get("/")
def bienvenida():
    return {"Bienvenida": "Bienvenido a la API de LobiFind"}
