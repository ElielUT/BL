from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.supabase_client import Base # Usamos la base que ya tienen en centro
from pydantic import BaseModel

class MateriaBase(BaseModel):
    nombre: str
    carrera: str
    cuatrimestre: int

class ImpartirBase(BaseModel):
    id_materia2: int
    id_asesor2: int
