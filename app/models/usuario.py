from pydantic import BaseModel, Field

regexCorreo = r"^[a-zA-Z0-9._%-]+@utsjr\.edu\.mx$"

class CrearUsuario(BaseModel):
    correo:str = Field(min_length=10, max_length=30, pattern=regexCorreo )
    nombres:str = Field(max_length=30)
    apellidos:str = Field(max_length=30)
    contraseña:str = Field()
    categoria:str = Field(max_length=15)
    cuatrimestre:int = Field(le=11, ge=1)
    plantel:str = Field(max_length=10)

class ActualizarUsuario(BaseModel):
    nombre:str | None = Field(max_length=30)
    apellidos:str | None = Field(max_length=30)
    contraseña:str | None = Field()
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
    correo:str
    contraseña:str

class ListaUsuario(BaseModel):
    items:list[RecuperarUsuarios]

class SoloUsuario(BaseModel):
    item:RecuperarUsuarios