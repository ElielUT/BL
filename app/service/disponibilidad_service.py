from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from postgrest import CountMethod 

def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_horario)

def crearDisponibilidad(data: dict):
    try:
        if not data:
            raise HTTPException(status_code=400, detail="Datos incompletos")

        hora_in_nueva = str(data.get("hora_in"))
        hora_fin_nueva = str(data.get("hora_fin"))

        # Verificar solapamiento con horarios existentes del mismo día
        existentes = _table().select("*") \
            .eq("id_asesor1", data.get("id_asesor1")) \
            .eq("dia", str(data.get("dia"))) \
            .execute()

        for h in (existentes.data or []):
            hora_in_ex = str(h.get("hora_in"))
            hora_fin_ex = str(h.get("hora_fin"))
            # Hay solapamiento si el nuevo horario se intersecta con alguno existente
            if hora_in_nueva < hora_fin_ex and hora_fin_nueva > hora_in_ex:
                raise HTTPException(
                    status_code=400,
                    detail=f"El horario se solapa con uno existente ({hora_in_ex[:5]} - {hora_fin_ex[:5]})"
                )

        data_json = jsonable_encoder(data)
        res = _table().insert(data_json).execute()
        return {"items": res.data[0] if res.data else None}

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear disponibilidad: {str(e)}")

def obtenerDisponibilidadPorAsesor(id_asesor: int):
    try:
        # Busca la columna de id_asesor1 que coincida con el id_asesor proporcionado
        res = _table().select("*").eq("id_asesor1", int(id_asesor)).order("dia").order("hora_in").execute()
        
        if not res.data:
            return {"items": [], "message": "No se encontró disponibilidad para este asesor"}
            
        return {"items": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener disponibilidad: {str(e)}")
