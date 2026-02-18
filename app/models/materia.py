from pydantic import BaseModel, Field

class CrearMateria(BaseModel):
    nombre: str = Field(min_length=1)
    carrera: str = Field(min_length=1)
    cuatrimestre: int = Field(ge=1)

class CrearImpartir(BaseModel):
    id_materia2: int = Field(ge=0)
    id_asesor2: int = Field(ge=0)
    
class RecuperarMateria(BaseModel):
    id_materia: int
    nombre: str
    carrera: str
    cuatrimestre: int

class RecuperarImpartir(BaseModel):
    id_impartir: int
    id_materia2: int
    id_asesor2: int
