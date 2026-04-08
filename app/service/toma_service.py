from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from postgrest import CountMethod


def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_toma)

def recuperarIDToma():
    try:
        id = _table().select(count=CountMethod.exact).execute()
        return {"id":id.count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al contar la cantidad de ingresos")
    
def crearToma(data:dict):
    try:
        if not data:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        data = jsonable_encoder(data)
        res = _table().insert(data).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la Toma {e}")

def estadisticas_asesorias():
    try:
        # Totales
        totales = _table().select("*", count=CountMethod.exact).execute()
        
        # Pendientes: sin fecha asignada
        pendientes = _table().select("*", count=CountMethod.exact).is_("fecha", "null").execute()
        
        # Aceptadas: con fecha, pero sin evaluacion
        aceptadas = _table().select("*", count=CountMethod.exact).not_.is_("fecha", "null").is_("calificacion", "null").execute()
        
        # Completadas: con evaluacion (mayor a cero usualmente, o simplemente no nula)
        completadas = _table().select("*", count=CountMethod.exact).not_.is_("calificacion", "null").execute()
        
        return {
            "totales": totales.count or 0,
            "pendientes": pendientes.count or 0,
            "aceptadas": aceptadas.count or 0,
            "completadas": completadas.count or 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas de tomas/asesorías: {e}")

def mostrar_Toma():
    try:
        res = _table().select(
            "*, asesoria(*, materia(*)), asesor!toma_id_asesor3_fkey(*, usuario!asesor_id_usuario2_fkey(*)), alumno!toma_id_alumno1_fkey(*, usuario!alumno_id_usuario1_fkey(*))"
        ).execute()
        return {"items": res.data if res.data else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tomas: {e}")

def buscar_TomaAsesor(id_asesor:int):
    try:
        res = _table().select(
            "*, asesoria(*, materia(*)), asesor(*, usuario(*)), alumno(*, usuario(*))"
        ).eq("id_asesor3", id_asesor).execute()
        print("DATA TOMA:", res.data)
        return {"items": res.data if res.data else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tomas del asesor: {e}")
    
def buscar_TomaAlumno(id_alumno:int):
    try:
        res = _table().select(
            "*, asesoria(*, materia(*)), asesor(*, usuario(*)), alumno(*, usuario(*))"
        ).eq("id_alumno1", id_alumno).execute()
        return {"items": res.data if res.data else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tomas del alumno: {e}")

def buscar_TomaAsesoria(id_asesoria:int):
    try:
        res = _table().select("*, asesoria(*, materia(*)), asesor(*, usuario(*)), alumno(*, usuario(*))").eq("id_asesoria2", id_asesoria).execute()
        return {"items": res.data if res.data else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la toma de la asesoria: {e}")
