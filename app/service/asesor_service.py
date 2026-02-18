from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from app.service.usuario_service import buscarUsuarioID
from app.service.materia_service import buscarMateriaNombre, buscarImpartirPorMateria
from app.service.usuario_service import buscarUsuarios

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
        return res.data[0] if res.data else None
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

def listarAsesores():
    try:
        res = _table().select("*").execute()
        return {"items":res.data if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar los Asesores {e}")

def buscarAsesorPorMateria(materia:str):
    try:
        if not materia:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        resMat = buscarMateriaNombre(materia)
        if not resMat:
            raise HTTPException(status_code=404, detail="Materia no encontrada")
        resImp = buscarImpartirPorMateria(resMat["id_materia"])
        if not resImp:
            raise HTTPException(status_code=404, detail="Impartir no encontrado")
        res = _table().select("*").eq("id_asesor", resImp["id_asesor2"]).execute()
        return {"items":res.data if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el Asesor {e}")

def buscarAsesorPorAsesorNombre(usuario:str):
    try:
        if not usuario:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        resUs = buscarUsuarios(usuario)
        if not resUs:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        res = _table().select("*").eq("id_usuario2", resUs["items"][0]["id_usuario"]).execute()
        return {"items":res.data if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el Asesor {e}")

def buscarAsesorPorAsesorID(id:int):
    try:
        if not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        res = _table().select("*").eq("id_asesor", int(id)).execute()
        return {"items":res.data if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el Asesor {e}")