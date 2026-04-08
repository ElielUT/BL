import uuid
from fastapi import HTTPException

def crear_meet_link() -> str:
    codigo = uuid.uuid4().hex[:8]
    return f"https://meet.jit.si/lobifind-{codigo}"