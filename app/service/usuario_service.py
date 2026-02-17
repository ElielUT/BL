from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from postgrest import CountMethod

def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_usuario)

def inicio(correo:str):
    try:
        res = _table().select("id_usuario, correo, contraseña, categaria").eq("correo", str(correo)).execute()
        if res:
            return {"Usuario": res.data}
        else:
            raise HTTPException(status_code=404, detail="Error al encontrar el usuario")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recuperar usuario {e}")
    
def recuperarIDUsuario():
    try:
        id = _table().select(count=CountMethod.exact).execute()
        return {"id":id.count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al contar la cantidad de ingresos")
    
def crearUsuario(datos:dict):
    try:
        if not datos:
            raise HTTPException(status_code=404, detail="Datos inexistentes")
        datos = jsonable_encoder(datos)
        res = _table().insert(datos).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar el usuario {e}")
    
def actualizarUsuario(id:int, datos:dict):
    try:
        if not datos or not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        datos = jsonable_encoder(datos)
        res = _table().update(datos).eq("id_usuario", int(id)).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario")
    
def eliminarUsuario(id:int):
    try:
        if not id:
            raise HTTPException(status_code=404, detail="ID faltante")
        res= _table().delete().eq("id_usuario", int(id)).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario {e}")