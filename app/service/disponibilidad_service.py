from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from postgrest import CountMethod 

def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table("horario")

def crearDisponibilidad(data: dict):
    try:
        if not data:
            raise HTTPException(status_code=400, detail="Datos incompletos")

        # 1. VALIDACIÓN DE DUPLICADOS: 
        # Verificamos si este asesor ya registró este bloque específico.
        # Convertimos dia y hora a string para la comparación en Supabase.
        existente = _table().select("*") \
            .eq("id_asesor1", data.get("id_asesor1")) \
            .eq("dia", str(data.get("dia"))) \
            .eq("hora_inicio", str(data.get("hora_inicio"))) \
            .execute()

        if existente.data:
            raise HTTPException(
                status_code=400, 
                detail=f"El asesor ya tiene este horario registrado (Día: {data.get('dia')}, Hora: {data.get('hora_inicio')})"
            )

        # 2. INSERCIÓN:
        # jsonable_encoder asegura que los datos estén en un formato compatible con JSON 
        data_json = jsonable_encoder(data)
        res = _table().insert(data_json).execute()
        
        # Retornar el registro creado
        return {"items": res.data[0] if res.data else None}

    except HTTPException as he:
        # Re-lanza los errores de validación
        raise he
    except Exception as e:
        # Errores inesperados de conexión o base de datos
        raise HTTPException(status_code=500, detail=f"Error al crear disponibilidad: {str(e)}")

def obtenerDisponibilidadPorAsesor(id_asesor: int):
    try:
        # Busca la columna de id_asesor1 que coincida con el id_asesor proporcionado
        res = _table().select("*").eq("id_asesor1", int(id_asesor)).execute()
        
        if not res.data:
            return {"items": [], "message": "No se encontró disponibilidad para este asesor"}
            
        return {"items": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener disponibilidad: {str(e)}")
