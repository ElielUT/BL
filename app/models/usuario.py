from pydantic import BaseModel, Field

class CrearUsuario(BaseModel):
    id_usuario:int = Field(ge=0)
    correo:str = Field(min_length=10, max_length=30)
    nombre:str = Field(max_length=30)
    apellidos:str = Field(max_length=30)
    contraseña:str = Field(max_length=20)
    categoria:str = Field(max_length=15)
    cuatrimestre:str = Field(max_length=25)
    plantel:str = Field(max_length=10)

class ActualizarUsuario(BaseModel):
    nombre:str | None = Field(max_length=30)
    apellidos:str | None = Field(max_length=30)
    contraseña:str | None = Field(max_length=20)
    categoria:str | None = Field(max_length=15)
    cuatrimestre:str | None = Field(max_length=25)
    plantel:str | None = Field(max_length=10)

class RecuperarUsuarios(BaseModel):
    id_usuario:int
    correo:str
    nombre:str
    apellidos:str
    categoria:str
    cuatrimestre:str
    plantel:str

class IniciarUsuario(BaseModel):
    id_usuario:int
    correo:str
    contraseña:str
    categoria:str

class ListaUsuario(BaseModel):
    items:list[RecuperarUsuarios]

class SoloUsuario(BaseModel):
    item:RecuperarUsuarios