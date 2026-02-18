from pydantic import BaseModel, Field

class CrearAsesoria(BaseModel):
    id_asesor3 : int = Field(ge=0)
    id_materia1 : str = Field(max_length=150)
    tema : str = Field(max_length=300)

class ActualizarAsesoria(BaseModel):
    id_materia1 : str | None = Field(max_length=150)
    tema : str | None = Field(max_length=300)

class RecuperarAsesoria(BaseModel):
    id_asesoria : int
    id_materia1 : str
    tema : str

class ListaAsesoria(BaseModel):
    items : list[RecuperarAsesoria]

class SoloAsesoria(BaseModel):
    item : RecuperarAsesoria
