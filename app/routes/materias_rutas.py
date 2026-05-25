#FastAPI y Supabase
from fastapi import APIRouter, Path

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

router = APIRouter()

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

@router.delete("/impartir/{id_impartir}", name="eliminarImpartir")
def eliminar_Impartir(id_impartir:int):
    return eliminar_impartir_db(id_impartir)

@router.delete("/impartir/asignacion/{id_materia}/{id_asesor}", name="desvincularAsesorMateria")
def desvincular_Asesor_Materia(id_materia:int, id_asesor:int):
    return desvincular_asignacion_db(id_materia, id_asesor)

@router.post("/impartir", response_model=CrearImpartir, name="crearImpartir")
def crear_Impartir(body:CrearImpartir):
    return asignar_impartir_db(body.model_dump())