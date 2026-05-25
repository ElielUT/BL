#FastAPI y Supabase
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

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

# ------------ RUTAS DE ALUMNO ---------------------------------
@router.post("/", response_model=RecuperarAlumno, status_code=201)
async def crear_nuevo_alumno(alumno: CrearAlumno):
    res = crearAlumno(alumno.model_dump())
    if not res:
        raise HTTPException(status_code=400, detail="No se pudo crear el alumno")
    return res

@router.get("/", response_model=ListaAlumnos)
async def obtener_todos_los_alumnos():
    return listarAlumnos()

@router.get("/{id_alumno}", response_model=SoloAlumno)
async def obtener_alumno_por_id(id_alumno: int):
    res = buscarAlumnoPorID(id_alumno)
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return {"item": res["items"]}

@router.put("/{id_alumno}", response_model=SoloAlumno)
async def actualizar_datos_alumno(id_alumno: int, datos: ActualizarAlumno):
    # Usamos exclude_unset=True para no enviar valores Nulos que no se quieran cambiar
    res = actualizarAlumno(id_alumno, datos.model_dump(exclude_unset=True))
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se encontró el alumno para actualizar")
    return {"item": res["items"]}

@router.delete("/{id_alumno}")
async def borrar_alumno(id_alumno: int):
    res = eliminarAlumno(id_alumno)
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo eliminar el alumno o no existe")
    return {"message": "Alumno eliminado exitosamente", "id": id_alumno}

@router.delete("/eliminarAlumnoForaneo/{id_alumno}")
async def borrar_alumno(id_alumno: int):
    res = eliminarAlumnoForaneo(id_alumno)
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo eliminar el alumno o no existe")
    return {"message": "Alumno eliminado exitosamente", "id": id_alumno}

@router.put("/actualizarAlumnoForaneo/{id_usuario}")
async def actualizar_alumno_foraneo(id_usuario: int, datos: dict):
    res = actualizarAlumnoForaneo(id_usuario, datos.get("carrera"))
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo actualizar el alumno o no existe")
    return {"message": "Alumno actualizado exitosamente", "id": id_usuario}
#------------------------------------------------------------------------