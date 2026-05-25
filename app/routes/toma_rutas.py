#FastAPI y Supabase
from fastapi import APIRouter, HTTPException
from app.core.supabase_client import get_supabase
from app.core.config import config

from app.models.toma import CrearToma, ListaToma, EstadisticasToma

from app.service.toma_service import crearToma, estadisticas_asesorias, mostrar_Toma, buscar_TomaAsesor, buscar_TomaAlumno, buscar_TomaAsesoria
from app.service.detalles_service import obtener_detalles_asesoria, guardar_meet_link
from app.service.meet_service import crear_meet_link

router = APIRouter(prefix="/toma", tags=["Toma"])

"""
Routes de Toma
"""
@router.post("/crearToma/", name="crearToma")
def crear_Toma(body:CrearToma):
    return crearToma(body.model_dump())

@router.get("/estadisticas", response_model=EstadisticasToma, name="estadisticasToma")
def obtener_estadisticas_toma():
    return estadisticas_asesorias()

@router.get("/mostrarToma/", response_model= ListaToma,name="mostrarToma")
def endpoint_mostrar_Toma():
    return mostrar_Toma()

@router.get("/buscarTomaAsesor/{id_asesor}", name="buscarTomaAsesor")
def endpoint_buscar_TomaAsesor(id_asesor:int):
    return buscar_TomaAsesor(id_asesor)

@router.get("/buscarTomaAlumno/{id_alumno}", name="buscarTomaAlumno")
def endpoint_buscar_TomaAlumno(id_alumno:int):
    return buscar_TomaAlumno(id_alumno)

@router.get("/buscarTomaAsesoria/{id_asesoria}", response_model=ListaToma, name="buscarTomaAsesoria")
def endpoint_buscar_TomaAsesoria(id_asesoria:int):
    return buscar_TomaAsesoria(id_asesoria)

@router.get("/detalles/{id_asesoria}", name="detallesAsesoria")
def endpoint_detalles_asesoria(id_asesoria: int):
    return obtener_detalles_asesoria(id_asesoria)

@router.post("/generarMeet/{id_asesor3}/{id_asesoria1}/{id_alumno1}", name="generarMeetLink")
def endpoint_generar_meet(id_asesor3: int, id_asesoria1: int, id_alumno1: int):
    meet_link = crear_meet_link()
    return guardar_meet_link(id_asesor3, id_asesoria1, id_alumno1, meet_link)

@router.put("/actualizarEstado/{id_asesor3}/{id_asesoria1}/{id_alumno1}", name="actualizarEstadoToma")
def endpoint_actualizar_estado(id_asesor3: int, id_asesoria1: int, id_alumno1: int, body: dict):
    try:
        sb = get_supabase()
        datos = {}
        if "estado" in body:
            datos["estado"] = body["estado"]
        if "calificacion" in body:
            datos["calificacion"] = body["calificacion"]
        res = sb.schema(config.supabase_schema).table(config.supabase_toma)\
            .update(datos)\
            .eq("id_asesor3", id_asesor3)\
            .eq("id_asesoria1", id_asesoria1)\
            .eq("id_alumno1", id_alumno1)\
            .execute()
        return {"success": True, "data": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar: {e}")

@router.delete("/cancelar/{id_asesor3}/{id_asesoria1}/{id_alumno1}", name="cancelarToma")
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

@router.post("/registrar/{id_asesor3}/{id_asesoria1}/{id_alumno1}", name="registrarToma")
def endpoint_registrar_toma(id_asesor3: int, id_asesoria1: int, id_alumno1: int):
    try:
        from datetime import datetime
        sb = get_supabase()
        
        # Obtener la toma
        res = sb.schema(config.supabase_schema).table(config.supabase_toma)\
            .select("*")\
            .eq("id_asesor3", id_asesor3)\
            .eq("id_asesoria1", id_asesoria1)\
            .eq("id_alumno1", id_alumno1)\
            .single()\
            .execute()
        
        if not res.data:
            raise HTTPException(status_code=404, detail="Toma no encontrada")
        
        toma = res.data
        fecha = toma.get("fecha")
        hora_fin = toma.get("hora_fin")
        
        if not fecha or not hora_fin:
            raise HTTPException(status_code=400, detail="La asesoría no tiene fecha u hora registrada")
        
        # Verificar que ya pasó la fecha y hora
        fecha_hora_fin = datetime.strptime(f"{fecha} {hora_fin}", "%Y-%m-%d %H:%M:%S")
        if datetime.now() < fecha_hora_fin:
            raise HTTPException(status_code=400, detail="La asesoría aún no ha terminado")
        
        # Cambiar estado a completada
        sb.schema(config.supabase_schema).table(config.supabase_toma)\
            .update({"estado": "completada"})\
            .eq("id_asesor3", id_asesor3)\
            .eq("id_asesoria1", id_asesoria1)\
            .eq("id_alumno1", id_alumno1)\
            .execute()
        
        # Liberar el slot del horario si existe
        id_horario = toma.get("id_horario")
        if id_horario:
            sb.schema(config.supabase_schema).table(config.supabase_horario)\
                .update({"disponible": True})\
                .eq("id_horario", id_horario)\
                .execute()
        
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar toma: {e}")