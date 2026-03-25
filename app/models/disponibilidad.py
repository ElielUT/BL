from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import date, time

class CrearDisponibilidad(BaseModel):
    model_config = ConfigDict(title="Crear Disponibilidad")

    # Forzamos a que tengan al menos 4 caracteres (valor >= 1000)
    id_horario: int = Field(ge=1, le=9999)
    id_asesor1: int = Field(ge=1, le=9999)
    dia: date
    hora_in: time
    hora_fin: time

    # --- Validaciones de tiempo ---

    @field_validator('hora_in', 'hora_fin')
    @classmethod
    def validar_30_minutos(cls, v: time):
        if v.minute not in [0, 30]:
            raise ValueError('Debe ser bloque de 30 min (:00 o :30)')
        return v

    @field_validator('hora_fin')
    @classmethod
    def validar_orden(cls, v: time, info):
        inicio = info.data.get('hora_in')
        if inicio and v <= inicio:
            raise ValueError("La hora de fin debe ser después del inicio")
        return v
