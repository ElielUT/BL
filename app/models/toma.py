from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional


class CrearToma(BaseModel):
    id_asesor3: int = Field(ge=0)
    id_asesoria1: int = Field(ge=0)
    id_alumno1: int = Field(ge=0)
    fecha: Optional[date] = None
    hora_in: Optional[time] = None
    hora_fin: Optional[time] = None
    calificacion: Optional[float] = Field(default=0, ge=0, le=5)

class RecuperarToma(BaseModel):
    id_asesor3: int
    id_asesoria1: int
    id_alumno1: int
    fecha: Optional[date] = None
    hora_in: Optional[time] = None
    hora_fin: Optional[time] = None
    calificacion: Optional[float] = None

class ListaToma(BaseModel):
    items:list[RecuperarToma]

class SoloToma(BaseModel):
    item:RecuperarToma

class EstadisticasToma(BaseModel):
    totales: int
    pendientes: int
    aceptadas: int
    completadas: int

class ActualizarMeetLink(BaseModel):
    meet_link: str = Field(max_length=500)

class DetallesAsesoria(BaseModel):
    id_toma: int
    materia: str
    tema: str
    nombre_asesorado: str
    nombre_asesor: str
    lugar: Optional[str] = "Reunión virtual"
    fecha: Optional[str] = None
    hora_in: Optional[str] = None
    hora_fin: Optional[str] = None
    duracion_min: Optional[int] = None
    fecha_solicitud: Optional[str] = None
    meet_link: Optional[str] = None
    calificacion: Optional[float] = None
    estado: str = "pendiente"  # pendiente | aceptada | completada