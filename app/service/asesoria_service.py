from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from postgrest import CountMethod

def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_asesoria)

def crearAsesoria(data:dict):
    try:
        if not data:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        data = jsonable_encoder(data)
        res = _table().insert(data).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear la Asesoria {e}")
    
def actualizarAsesoria(id:int,datos:dict):
    try:
        if not datos or not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        datos = jsonable_encoder(datos)
        res = _table().update(datos).eq("id_asesoria", int(id)).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la Asesoria {e}")
    
def eliminarAsesoria(id:int):
    try:
        if not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        res = _table().delete().eq("id_asesoria", int(id)).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la Asesoria {e}")

def mostrar_asesoria_supervisar():
    try:
        # Se obtiene desde la vista de asesoria con asociaciones clave via PostgREST de Supabase
        res = _table().select("*, materia(*), toma(*, asesor(*, usuario(*)), alumno(*, usuario(*)))").execute()
        return {"items": res.data if res.data else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener asesorías (supervisión): {e}")

def estadisticas_asesoria_supervisar():
    try:
        res = _table().select("*, toma(estado)").execute()
        data = res.data if res.data else []
        totales = len(data)
        pendientes = 0
        aceptadas = 0
        completadas = 0
        
        for item in data:
            if item.get("toma") and len(item["toma"]) > 0:
                toma_item = item["toma"][0]
                estado = toma_item.get("estado")
                # Si el estado no está mapeado aún, lo estimamos o lo leemos si es str
                if estado == "Pendiente":
                    pendientes += 1
                elif estado == "Aceptada" or estado == "Aceptado":
                    aceptadas += 1
                elif estado == "Completadas" or estado == "Completada":
                    completadas += 1
                else: 
                    # Por defecto o null -> Pendiente
                    pendientes += 1
            else:
                # Si no hay match de toma para asesoria (anomalía), por defecto puede ser pendiente
                pendientes += 1

        return {
            "totales": totales,
            "pendientes": pendientes,
            "aceptadas": aceptadas,
            "completadas": completadas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener estadísticas de asesorías (supervisión): {e}")