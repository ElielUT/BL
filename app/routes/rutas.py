from fastapi import APIRouter, Path, Query
from app.models.usuario import CrearUsuario, ActualizarUsuario, RecuperarUsuarios, IniciarUsuario, ListaUsuario, SoloUsuario
from app.service.usuario_service import inicio, crearUsuario, eliminarUsuario, actualizarUsuario
from app.service.encryptar import descifrar

router = APIRouter()

@router.get("/")
def bienvenida():
    return "Bienvenido a la API de LobiFind"

@router.post("/inicio", name= "IniciarSesion")
def iniciarSesion(body:IniciarUsuario):
    res = inicio(body.correo)
    cc = res["contraseña"]
    cnc = descifrar(cc)
    if(res["contraseña"] == cc):
        if(res["categoria"] == "asesor"):
            return {"Inicio": 1}
        elif(res["categoria"] == "alumno"):
            return {"Inicio": 2}
        elif(res["categoria"] == "admin"):
            return {"Inicio": 3}
    else:
        return {"Inicio": False}
    
@router.post("/crearUsuario", response_model=CrearUsuario,name="crearUsuario")
def crear_Usuario(body:CrearUsuario):
    return crearUsuario(body.model_dump())

@router.get("/eliminarUsuario/{id_usuario}", name="eliminarUsuario")
def eliminar_Usuario(id_usuario:int):
    return eliminarUsuario(id_usuario)

@router.put("/actualizarUsuario/{id_usurio}", response_model=ActualizarUsuario, name="actualizarUsuario")
def actualizar_Usuario(id_usuario:int, body:ActualizarUsuario):
    return actualizarUsuario(id_usuario, body.model_dump(exclude_none=True))