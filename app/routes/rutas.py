from fastapi import APIRouter, Path, Query
from app.core.supabase_client import get_supabase
from app.core.config import config
from app.models.asesoria import ActualizarAsesoria, CrearAsesoria, ListaAsesoria, SoloAsesoria
from app.models.toma import CrearToma, ListaToma, EstadisticasToma
from app.models.usuario import CrearUsuario, ActualizarUsuario, IniciarUsuario, ListaUsuario, SoloUsuario, CantidadUsuarios
from app.service.disponibilidad_service import obtenerDisponibilidadPorAsesor, crearDisponibilidad
from app.models.disponibilidad import CrearDisponibilidad
from app.service.usuario_service import inicio, crearUsuario, eliminarUsuario, actualizarUsuario, listarUsuarios, buscarUsuarios, buscarUsuarioID, cantidadUsuarios
from app.models.asesor import CrearAsesor, ActualizarAsesor, ListaAsesor, SoloAsesor 
from app.service.asesor_service import eliminarAsesor, crearAsesor, actualizarAsesor, listarAsesores, buscarAsesorPorMateria, buscarAsesorPorAsesorNombre, buscarAsesorPorAsesorID, eliminarAsesorForaneo, actualizarAsesorForaneo
from app.service.encryptar import descifrar
from app.models.disponibilidad import CrearDisponibilidad
from app.service.disponibilidad_service import obtenerDisponibilidadPorAsesor, crearDisponibilidad
#from app.core.supabase_client import get_db
from app.models.materia import CrearMateria, RecuperarMateria, CrearImpartir, RecuperarImpartir
from app.service.materia_service import (
    crear_materia_db,
    asignar_impartir_db,
    listar_materias_db,
    obtener_materia_db,
    actualizar_materia_db,
    eliminar_materia_db,
    listar_impartir_db,
    obtener_impartir_db,
    actualizar_impartir_db,
    eliminar_impartir_db,
    desvincular_asignacion_db
)
from fastapi import APIRouter, HTTPException
from app.models.alumnos import CrearAlumno, ActualizarAlumno, RecuperarAlumno, ListaAlumnos, SoloAlumno
from app.service.alumno_service import (
    crearAlumno, 
    actualizarAlumno, 
    eliminarAlumno, 
    eliminarAlumnoForaneo,
    actualizarAlumnoForaneo,
    listarAlumnos, 
    buscarAlumnoPorID
)

# Importaciones para las rutas de Toma y Asesoría
from app.service.toma_service import crearToma, estadisticas_asesorias, mostrar_Toma, buscar_TomaAsesor, buscar_TomaAlumno, buscar_TomaAsesoria
from app.service.asesoria_service import crearAsesoria, eliminarAsesoria, actualizarAsesoria
from app.service.detalles_service import obtener_detalles_asesoria, guardar_meet_link
from app.service.meet_service import crear_meet_link
from app.models.toma import ActualizarMeetLink

router = APIRouter()

@router.get("/")
def bienvenida():
    return {"Bienvenida": "Bienvenido a la API de LobiFind"}

"""
Routes de Usuarios
"""
@router.post("/usuarios/inicio", name= "IniciarSesion")
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
    
@router.post("/usuarios/crearUsuario", name="crearUsuario")
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

@router.get("/usuarios/buscarUsuarios/{correo}", response_model=SoloUsuario, name="buscarUsuarios")
def buscar_Usuarios(correo:str):
    return buscarUsuarios(correo)

@router.get("/usuarios/buscarUsuarioID/{id_usuario}", response_model=SoloUsuario, name="buscarUsuarioID")
def buscar_UsuarioID(id_usuario:int):
    return buscarUsuarioID(id_usuario)

@router.get("/usuarios/cantidadUsuarios", response_model=CantidadUsuarios, name="cantidadUsuarios")
def cantidad_Usuarios():
    return cantidadUsuarios()

"""
Routes de Asesores
"""
@router.post("/asesores/crearAsesor", response_model=CrearAsesor, name="crearAsesor")
def crear_Asesor(body:CrearAsesor):
    return crearAsesor(body.model_dump())

@router.get("/asesores/eliminarAsesor/{id_asesor}", name="eliminarAsesor")
def eliminar_Asesor(id_asesor:int):
    return eliminarAsesor(id_asesor)

@router.put("/asesores/actualizarAsesor/{id_asesor}", response_model=ActualizarAsesor, name="actualizarAsesor")
def actualizar_Asesor(id_asesor:int, body:ActualizarAsesor):
    return actualizarAsesor(id_asesor, body.model_dump(exclude_none=True))

@router.get("/asesores/listarAsesores", response_model=ListaAsesor, name="listarAsesores")
def listar_Asesores():
    return listarAsesores()

@router.get("/asesores/buscarAsesorMateria/{materia}", response_model=ListaAsesor, name="buscarAsesorMateria")
def buscar_Asesor(materia:str):
    return buscarAsesorPorMateria(materia)

@router.get("/asesores/buscarAsesorUsuario/{usuario}", response_model=ListaAsesor, name="buscarAsesorUsuario")
def buscar_AsesorUsuario(usuario:str):
    return buscarAsesorPorAsesorNombre(usuario)

@router.get("/asesores/buscarAsesorID/{id_asesor}", response_model=SoloAsesor, name="buscarAsesorID")
def buscar_AsesorID(id_asesor:int):
    return buscarAsesorPorAsesorID(id_asesor)

@router.delete("/asesores/eliminarAsesorForaneo/{id_asesor}")
async def borrar_asesor(id_asesor: int):
    res = eliminarAsesorForaneo(id_asesor)
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo eliminar el asesor o no existe")
    return {"message": "Asesor eliminado exitosamente", "id": id_asesor}

@router.put("/asesores/actualizarAsesorForaneo/{id_usuario}")
async def actualizar_asesor_foraneo(id_usuario: int, datos: dict):
    res = actualizarAsesorForaneo(id_usuario, datos.get("carrera"))
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo actualizar el asesor o no existe")
    return {"message": "Asesor actualizado exitosamente", "id": id_usuario}

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
Routes de Toma
"""
@router.post("/toma/crearToma/", name="crearToma")
def crear_Toma(body:CrearToma):
    return crearToma(body.model_dump())

@router.get("/toma/estadisticas", response_model=EstadisticasToma, name="estadisticasToma")
def obtener_estadisticas_toma():
    return estadisticas_asesorias()

@router.get("/toma/mostrarToma/", response_model= ListaToma,name="mostrarToma")
def endpoint_mostrar_Toma():
    return mostrar_Toma()

@router.get("/toma/buscarTomaAsesor/{id_asesor}", name="buscarTomaAsesor")
def endpoint_buscar_TomaAsesor(id_asesor:int):
    return buscar_TomaAsesor(id_asesor)

@router.get("/toma/buscarTomaAlumno/{id_alumno}", name="buscarTomaAlumno")
def endpoint_buscar_TomaAlumno(id_alumno:int):
    return buscar_TomaAlumno(id_alumno)

@router.get("/toma/buscarTomaAsesoria/{id_asesoria}", response_model=ListaToma, name="buscarTomaAsesoria")
def endpoint_buscar_TomaAsesoria(id_asesoria:int):
    return buscar_TomaAsesoria(id_asesoria)

@router.get("/toma/detalles/{id_asesoria}", name="detallesAsesoria")
def endpoint_detalles_asesoria(id_asesoria: int):
    return obtener_detalles_asesoria(id_asesoria)

@router.post("/toma/generarMeet/{id_asesor3}/{id_asesoria1}/{id_alumno1}", name="generarMeetLink")
def endpoint_generar_meet(id_asesor3: int, id_asesoria1: int, id_alumno1: int):
    meet_link = crear_meet_link()
    return guardar_meet_link(id_asesor3, id_asesoria1, id_alumno1, meet_link)

@router.put("/toma/actualizarEstado/{id_asesor3}/{id_asesoria1}/{id_alumno1}", name="actualizarEstadoToma")
def endpoint_actualizar_estado(id_asesor3: int, id_asesoria1: int, id_alumno1: int, body: dict):
    try:
        sb = get_supabase()
        res = sb.schema(config.supabase_schema).table(config.supabase_toma)\
            .update({"estado": body.get("estado")})\
            .eq("id_asesor3", id_asesor3)\
            .eq("id_asesoria1", id_asesoria1)\
            .eq("id_alumno1", id_alumno1)\
            .execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar estado: {e}")

"""
Routes de Asesoria
"""
@router.post("/asesoria/crearAsesoria", name="crearAsesoria")
def crear_Asesoria(body:CrearAsesoria):
    return crearAsesoria(body.model_dump())

@router.get("/asesoria/eliminarAsesoria/{id_asesoria}", name="eliminarAsesoria")
def eliminar_Asesoria(id_asesoria:int):
    return eliminarAsesoria(id_asesoria)

@router.put("/asesoria/actualizarAsesoria/{id_asesoria}", response_model=ActualizarAsesoria, name="actualizarAsesoria")
def actualizar_Asesoria(id_asesoria:int, body:ActualizarAsesoria):
    return actualizarAsesoria(id_asesoria, body.model_dump(exclude_none=True))

@router.delete("/impartir/{id_impartir}", name="eliminarImpartir")
def eliminar_Impartir(id_impartir:int):
    return eliminar_impartir_db(id_impartir)

@router.delete("/impartir/asignacion/{id_materia}/{id_asesor}", name="desvincularAsesorMateria")
def desvincular_Asesor_Materia(id_materia:int, id_asesor:int):
    return desvincular_asignacion_db(id_materia, id_asesor)

@router.post("/impartir", response_model=CrearImpartir, name="crearImpartir")
def crear_Impartir(body:CrearImpartir):
    return asignar_impartir_db(body.model_dump())

# ------------ RUTAS DE DISPONIBILIDAD ---------------------------------
# Obtener la disponibilidad de un asesor
@router.get("/disponibilidad/{id_asesor}", name="obtenerDisponibilidad")
def obtener_disponibilidad(id_asesor: int = Path(..., ge=0)):
    return obtenerDisponibilidadPorAsesor(id_asesor)

# Crear una nueva disponibilidad
@router.post("/disponibilidad", name="CrearDisponibilidad")
def crear_nueva_disponibilidad(data: CrearDisponibilidad):
    # Llamamos a la función del SERVICE pasándole el diccionario de datos
    return crearDisponibilidad(data.model_dump())
#------------------------------------------------------------------------

# ------------ RUTAS DE ALUMNO ---------------------------------
@router.post("/alumnos", response_model=RecuperarAlumno, status_code=201)
async def crear_nuevo_alumno(alumno: CrearAlumno):
    res = crearAlumno(alumno.model_dump())
    if not res:
        raise HTTPException(status_code=400, detail="No se pudo crear el alumno")
    return res

@router.get("/alumnos", response_model=ListaAlumnos)
async def obtener_todos_los_alumnos():
    return listarAlumnos()

@router.get("/alumnos/{id_alumno}", response_model=SoloAlumno)
async def obtener_alumno_por_id(id_alumno: int):
    res = buscarAlumnoPorID(id_alumno)
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return {"item": res["items"]}

@router.put("/alumnos/{id_alumno}", response_model=SoloAlumno)
async def actualizar_datos_alumno(id_alumno: int, datos: ActualizarAlumno):
    # Usamos exclude_unset=True para no enviar valores Nulos que no se quieran cambiar
    res = actualizarAlumno(id_alumno, datos.model_dump(exclude_unset=True))
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se encontró el alumno para actualizar")
    return {"item": res["items"]}

@router.delete("/alumnos/{id_alumno}")
async def borrar_alumno(id_alumno: int):
    res = eliminarAlumno(id_alumno)
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo eliminar el alumno o no existe")
    return {"message": "Alumno eliminado exitosamente", "id": id_alumno}

@router.delete("/alumnos/eliminarAlumnoForaneo/{id_alumno}")
async def borrar_alumno(id_alumno: int):
    res = eliminarAlumnoForaneo(id_alumno)
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo eliminar el alumno o no existe")
    return {"message": "Alumno eliminado exitosamente", "id": id_alumno}

@router.put("/alumnos/actualizarAlumnoForaneo/{id_usuario}")
async def actualizar_alumno_foraneo(id_usuario: int, datos: dict):
    res = actualizarAlumnoForaneo(id_usuario, datos.get("carrera"))
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo actualizar el alumno o no existe")
    return {"message": "Alumno actualizado exitosamente", "id": id_usuario}
#------------------------------------------------------------------------


@router.delete("/toma/cancelar/{id_asesor3}/{id_asesoria1}/{id_alumno1}", name="cancelarToma")
def endpoint_cancelar_toma(id_asesor3: int, id_asesoria1: int, id_alumno1: int):
    try:
        sb = get_supabase()
        # 1. Borrar la toma
        sb.schema(config.supabase_schema).table(config.supabase_toma)\
            .delete()\
            .eq("id_asesor3", id_asesor3)\
            .eq("id_asesoria1", id_asesoria1)\
            .eq("id_alumno1", id_alumno1)\
            .execute()
        # 2. Borrar la asesoria
        sb.schema(config.supabase_schema).table(config.supabase_asesoria)\
            .delete()\
            .eq("id_asesoria", id_asesoria1)\
            .execute()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al cancelar: {e}")