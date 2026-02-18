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
    