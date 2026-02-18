from fastapi import APIRouter, Path, Query
from app.models.usuario import CrearUsuario, ActualizarUsuario, IniciarUsuario, ListaUsuario
from app.service.usuario_service import inicio, crearUsuario, eliminarUsuario, actualizarUsuario, listarUsuarios, buscarUsuarios
from app.service.encryptar import descifrar
from app.models.materia import CrearMateria, RecuperarMateria, CrearImpartir, RecuperarImpartir
from app.service.materia_service import (
    crear_materia_db,
    asignar_impartir_db,
    listar_materias_db,
    obtener_materia_db,
    actualizar_materia_db,
    eliminar_materia_db,
)
from app.models.asesor import CrearAsesor
from app.service.asesor_service import crearAsesor


router = APIRouter()

@router.get("/")
def bienvenida():
    return "Bienvenido a la API de LobiFind"

"""
Routes de Usuarios
"""
@router.post("/usuarios/inicio", name= "IniciarSesion")
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
    
@router.post("/usuarios/crearUsuario", response_model=CrearUsuario,name="crearUsuario")
def crear_Usuario(body:CrearUsuario):
    return crearUsuario(body.model_dump())

@router.get("/usuarios/eliminarUsuario/{id_usuario}", name="eliminarUsuario")
def eliminar_Usuario(id_usuario:int):
    return eliminarUsuario(id_usuario)

@router.put("/usuarios/actualizarUsuario/{id_usurio}", response_model=ActualizarUsuario, name="actualizarUsuario")
def actualizar_Usuario(id_usuario:int, body:ActualizarUsuario):
    return actualizarUsuario(id_usuario, body.model_dump(exclude_none=True))

@router.get("/usuarios/mostraUsuarios", response_model=ListaUsuario, name="mostrarUsuarios")
def mostrar_Usuarios():
    return listarUsuarios()

@router.get("/usuarios/buscarUsuarios/{nombre}", response_model=ListaUsuario, name="buscarUsuarios")
def buscar_Usuarios(nombre:str):
    return buscarUsuarios(nombre)

"""
Routes de Asesores
"""
@router.post("/asesores/crearAsesor", response_model=CrearAsesor, name="crearAsesor")
def crear_Asesor(body:CrearAsesor):
    return crearAsesor(body.model_dump())

"""
Routes de Materias
"""
@router.post("/materias/crear", response_model=CrearMateria, name="crearMateria")
def crear_Materia(body:CrearMateria):
    return crear_materia_db(body.model_dump())

@router.get("/materias", name="listarMaterias")
def listar_Materias():
    return listar_materias_db()

@router.get("/materias/{id_materia}", name="obtenerMateria")
def obtener_Materia(id_materia:int = Path(..., ge=1)):
    return obtener_materia_db(id_materia)

@router.put("/materias/{id_materia}", name="actualizarMateria")
def actualizar_Materia(id_materia:int, body:CrearMateria):
    return actualizar_materia_db(id_materia, body.model_dump(exclude_none=True))

@router.delete("/materias/{id_materia}", name="eliminarMateria")
def eliminar_Materia(id_materia:int):
    return eliminar_materia_db(id_materia)

"""
Routes de Impartir
"""
@router.post("/impartir/asignar", response_model=CrearImpartir, name="asignarImpartir")
def asignar_Impartir(body:CrearImpartir):
    return asignar_impartir_db(body.model_dump())