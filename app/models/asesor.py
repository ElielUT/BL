from pydantic import BaseModel, Field
from typing import Optional

class CrearAsesor(BaseModel):
    id_usuario2:int = Field(ge=0)
    carrera:str = Field(max_length=150)
    disponible:bool
    categoria:str = Field(max_length=15)
    contacto:str = Field(max_length=30)

class ActualizarAsesor(BaseModel):
    carrera:str | None = Field(max_length=150)
    disponible:bool | None
    categoria:str | None = Field(max_length=15)
    contacto:str | None = Field(max_length=30)

class RecuperarAsesor(BaseModel):
    id_asesor:int
    id_usuario2:int
    carrera:str
    disponible:bool
    categoria:str
    contacto:str
    # Campos adicionales del usuario (opcionales)
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    correo_usuario: Optional[str] = None
    usuario: Optional[dict] = None

class ListaAsesor(BaseModel):
    items: list[RecuperarAsesor]

class SoloAsesor(BaseModel):
    item: RecuperarAsesor