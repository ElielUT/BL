#FastAPI y Supabase
from fastapi import APIRouter, Path, HTTPException
from app.core.supabase_client import get_supabase
from app.core.config import config

from app.models.disponibilidad import CrearDisponibilidad

from app.service.disponibilidad_service import obtenerDisponibilidadPorAsesor, crearDisponibilidad

router = APIRouter(prefix="/disponibilidad", tags=["Disponibilidad"])

# ------------ RUTAS DE DISPONIBILIDAD ---------------------------------
# Obtener la disponibilidad de un asesor
@router.get("/{id_asesor}", name="obtenerDisponibilidad")
def obtener_disponibilidad(id_asesor: int = Path(..., ge=0)):
    return obtenerDisponibilidadPorAsesor(id_asesor)

# Crear una nueva disponibilidad
@router.post("", name="CrearDisponibilidad")
def crear_nueva_disponibilidad(data: CrearDisponibilidad):
    # Llamamos a la función del SERVICE pasándole el diccionario de datos
    return crearDisponibilidad(data.model_dump())

@router.put("/actualizarDisponible/{id_horario}", name="actualizarDisponible")
def actualizar_disponible(id_horario: int, body: dict):
    try:
        sb = get_supabase()
        res = sb.schema(config.supabase_schema).table(config.supabase_horario)\
            .update({"disponible": body.get("disponible")})\
            .eq("id_horario", id_horario)\
            .execute()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar disponibilidad: {e}")

@router.delete("/eliminarDisponibilidad/{id_horario}", name="eliminarDisponibilidad")
def eliminar_disponibilidad(id_horario: int):
    try:
        sb = get_supabase()
        res = sb.schema(config.supabase_schema).table(config.supabase_horario)\
            .delete()\
            .eq("id_horario", id_horario)\
            .execute()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar disponibilidad: {e}")