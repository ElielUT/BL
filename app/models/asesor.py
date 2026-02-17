from pydantic import BaseModel, Field

class CrearAsesor(BaseModel):
    id_asesor:int = Field(ge=0)
    id_usuario2:int = Field(ge=0)
    carrera:str = Field(max_length=150)
    disponible:bool
    categoria:str = Field(max_length=15)
    contacto:str = Field(max_length=30)

class ActualizarUsuario(BaseModel):
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

class ListaAsesor(BaseModel):
    items:list[RecuperarAsesor]

class SoloAsesor(BaseModel):
    item:RecuperarAsesor