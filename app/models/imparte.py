from pydantic import BaseModel, Field

class CrearImparte(BaseModel):
    id_materia2: int = Field(ge=0)
    id_asesor2: int = Field(ge=0)

class RecuperarImparte(BaseModel):
    id_impartir: int
    id_materia2: int
    id_asesor2: int

class ActualizarImparte(BaseModel):
    id_materia2: int = Field(ge=0)
    id_asesor2: int = Field(ge=0)

class EliminarImparte(BaseModel):
    id_impartir: int