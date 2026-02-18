from fastapi import APIRouter, Path, Query
from app.models.toma import CrearToma, ListaToma
from app.models.usuario import CrearUsuario, ActualizarUsuario, IniciarUsuario, ListaUsuario
from app.service.toma_service import crearToma
from app.service.usuario_service import inicio, crearUsuario, eliminarUsuario, actualizarUsuario, listarUsuarios, buscarUsuarios
from app.service.encryptar import descifrar
from app.core.supabase_client import get_db
from app.models.materia import CrearMateria, RecuperarMateria, CrearImpartir, RecuperarImpartir
from app.service.materia_service import crear_materia_db, asignar_impartir_db
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

@router.put("/usuarios/actualizarUsuario/{id_usuario}", response_model=ActualizarUsuario, name="actualizarUsuario")
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
Routes de Toma
"""
@router.get("/toma/crearToma/", response_model= CrearToma ,name="crearToma")
def crear_Toma(body:CrearToma):
    return crearToma(body.model_dump())

@router.get("/toma/mostrarToma/", response_model= ListaToma,name="mostrarToma")
def mostrar_Toma():
    return mostrar_Toma()

@router.get("/toma/buscarTomaAsesor/{id_asesor}", response_model=ListaToma, name="buscarTomaAsesor")
def buscar_TomaAsesor(id_asesor:int):
    return buscar_TomaAsesor(id_asesor)

@router.get("/toma/buscarTomaAlumno/{id_alumno}", response_model=ListaToma, name="buscarTomaAlumno")
def buscar_TomaAlumno(id_alumno:int):
    return buscar_TomaAlumno(id_alumno)

@router.get("/toma/buscarTomaAsesoria/{id_asesoria}", response_model=ListaToma, name="buscarTomaAsesoria")
def buscar_TomaAsesoria(id_asesoria:int):
    return buscar_TomaAsesoria(id_asesoria)

"""
Routes de Asesoria
"""

