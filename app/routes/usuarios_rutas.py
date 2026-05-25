#FastAPI y Supabase
from fastapi import APIRouter

from app.models.usuario import CrearUsuario, ActualizarUsuario, IniciarUsuario, ListaUsuario, SoloUsuario, CantidadUsuarios, CambiarContraseña

from app.service.usuario_service import inicio, crearUsuario, eliminarUsuario, actualizarUsuario, listarUsuarios, buscarUsuarios, buscarUsuarioID, cantidadUsuarios, cambiarContraseña

from app.service.encryptar import descifrar

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

"""
Routes de Usuarios
"""
@router.post("/inicio", name= "IniciarSesion")
def iniciarSesion(body:IniciarUsuario):
    if(body.correo == "admin" and body.contraseña == "admin"):
        return {"Inicio": 3}
    else:
        res = inicio(body.correo)
        cc = res["contraseña"]
        cnc = descifrar(cc)
        if(cnc == body.contraseña):
            if(res["categoria"] == "asesor"):
                from app.service.asesor_service import buscarAsesorPorAsesorNombre
                asesor_info = buscarAsesorPorAsesorNombre(body.correo)
                id_asesor = asesor_info["items"][0]["id_asesor"] if asesor_info.get("items") else None
                return {"Inicio": 1,
                        "id_usuario": res["id_usuario"],
                        "id_asesor": id_asesor}
            elif(res["categoria"] == "asesorado"):
                from app.service.alumno_service import listarAlumnos
                alumnos_res = listarAlumnos()
                # Buscar el id_alumno filtrando por id_usuario
                id_alumno = None
                if alumnos_res and alumnos_res.get("items"):
                    for a in alumnos_res["items"]:
                        if a.get("id_usuario1") == res["id_usuario"]:
                            id_alumno = a.get("id_alumno")
                            break
                return {"Inicio": 2,
                        "id_usuario": res["id_usuario"],
                        "id_alumno": id_alumno}
            elif(res["categoria"] == "admin"):
                return {"Inicio": 3,
                        "id_usuario": 1} # O el ID del admin si lo hay en la DB
        else:
            return {"Inicio": False}
    
@router.post("/crearUsuario", name="crearUsuario")
def crear_Usuario(body:CrearUsuario):
    return crearUsuario(body.model_dump())

@router.get("/eliminarUsuario/{id_usuario}", name="eliminarUsuario")
def eliminar_Usuario(id_usuario:int):
    return eliminarUsuario(id_usuario)

@router.put("/actualizarUsuario/{id_usuario}", response_model=ActualizarUsuario, name="actualizarUsuario")
def actualizar_Usuario(id_usuario:int, body:ActualizarUsuario):
    return actualizarUsuario(id_usuario, body.model_dump(exclude_none=True))

@router.get("/mostraUsuarios", response_model=ListaUsuario, name="mostrarUsuarios")
def mostrar_Usuarios():
    return listarUsuarios()

@router.get("/buscarUsuarios/{correo}", response_model=SoloUsuario, name="buscarUsuarios")
def buscar_Usuarios(correo:str):
    return buscarUsuarios(correo)

@router.get("/buscarUsuarioID/{id_usuario}", response_model=SoloUsuario, name="buscarUsuarioID")
def buscar_UsuarioID(id_usuario:int):
    return buscarUsuarioID(id_usuario)

@router.get("/cantidadUsuarios", response_model=CantidadUsuarios, name="cantidadUsuarios")
def cantidad_Usuarios():
    return cantidadUsuarios()

@router.put("/cambiarContraseña/{id_usuario}", name="cambiarContraseña")
def cambiar_Contraseña(id_usuario:int, body:CambiarContraseña):
    return cambiarContraseña(id_usuario, body.model_dump(exclude_none=True))