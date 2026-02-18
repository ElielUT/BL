from pydantic import BaseModel, Field
from datetime import date, time

class CrearToma(BaseModel):
    id_asesor3: int = Field(ge=0)
    id_asesoria1: int = Field(ge=0)
    id_alumno1: int = Field(ge=0)
    fecha : date = Field(default_factory= None)
    hora_in: time = Field(default_factory= None)
    hora_fin: time = Field(default_factory= None)
    evaluacion_ase : float = Field(ge=0, le=5)

class RecuperarToma(BaseModel):
    id_asesor3: int
    id_asesoria1: int
    id_alumno1: int
    fecha : date
    hora_in: time
    hora_fin: time
    evaluacion_ase : float

class ListaToma(BaseModel):
    items:list[RecuperarToma]

class SoloToma(BaseModel):
    item:RecuperarToma