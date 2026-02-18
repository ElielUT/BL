from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from app.service.usuario_service import buscarUsuarioID

def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_asesor)

def crearAsesor(data:dict):
    try:
        if not data:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        res = buscarUsuarioID(data["id_usuario2"])
        if not res:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        data = jsonable_encoder(data)
        res = _table().insert(data).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el Asesor {e}")
    
def actualizarAsesor(id:int,datos:dict):
    try:
        if not datos or not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        datos = jsonable_encoder(datos)
        res = _table().update(datos).eq("id_asesor", int(id)).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el Asesor {e}")
    
def eliminarAsesor(id:int):
    try:
        if not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        res = _table().delete().eq("id_asesor", int(id)).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el Asesor {e}")