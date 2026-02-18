from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config

def _table_materia():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_materia)

def _table_impartir():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_imparte)

def _table_asesor():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_asesor)

def crear_materia_db(datos: dict):
    try:
        if not datos:
            raise HTTPException(status_code=400, detail="Datos incompletos")
            
        # Validar nombre duplicado
        existe = _table_materia().select("*").eq("nombre", datos["nombre"]).execute()
        if existe.data:
            raise HTTPException(status_code=400, detail="Materia ya registrada")
            
        datos = jsonable_encoder(datos)
        res = _table_materia().insert(datos).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear materia: {e}")

def asignar_impartir_db(datos: dict):
    try:
        # Validar existencia de materia
        m_existe = _table_materia().select("id_materia").eq("id_materia", datos["id_materia2"]).execute()
        if not m_existe.data:
             raise HTTPException(status_code=404, detail="Materia no encontrada")

        # Validar existencia de asesor
        a_existe = _table_asesor().select("id_asesor").eq("id_asesor", datos["id_asesor2"]).execute()
        if not a_existe.data:
             raise HTTPException(status_code=404, detail="Asesor no encontrado")

        datos = jsonable_encoder(datos)
        res = _table_impartir().insert(datos).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al asignar materia: {e}")

def listar_materias_db():
    try:
        res = _table_materia().select("*").execute()
        return {"items": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar materias: {e}")

def obtener_materia_db(id:int):
    try:
        res = _table_materia().select("*").eq("id_materia", int(id)).execute()
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener materia: {e}")

def actualizar_materia_db(id:int, datos:dict):
    try:
        if not datos or not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        datos = jsonable_encoder(datos)
        res = _table_materia().update(datos).eq("id_materia", int(id)).execute()
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar materia: {e}")

def eliminar_materia_db(id:int):
    try:
        if not id:
            raise HTTPException(status_code=404, detail="ID faltante")
        res = _table_materia().delete().eq("id_materia", int(id)).execute()
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar materia: {e}")

def listar_impartir_db():
    try:
        res = _table_impartir().select("*").execute()
        return {"items": res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar impartir: {e}")

def obtener_impartir_db(id:int):
    try:
        res = _table_impartir().select("*").eq("id_impartir", int(id)).execute()
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"DEBUG obtener_impartir_db: {e}\n{tb}")
        raise HTTPException(status_code=500, detail=f"Error al obtener impartir: {str(e)}\n{tb}")

def actualizar_impartir_db(id:int, datos:dict):
    try:
        if not datos or not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        datos = jsonable_encoder(datos)
        res = _table_impartir().update(datos).eq("id_impartir", int(id)).execute()
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar impartir: {e}")

def eliminar_impartir_db(id:int):
    try:
        if not id:
            raise HTTPException(status_code=404, detail="ID faltante")
        res = _table_impartir().delete().eq("id_impartir", int(id)).execute()
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"DEBUG eliminar_impartir_db: {e}\n{tb}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar impartir: {str(e)}\n{tb}")

def buscarMateriaNombre(nombre:str):
    try:
        res = _table_materia().select("*").eq("nombre", nombre).execute()
        print(res.data)
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar materia: {e}")

def buscarImpartirPorMateria(id_materia:int):
    try:
        res = _table_impartir().select("*").eq("id_materia2", id_materia).execute()
        print(res.data)
        return res.data[0] if res.data else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar impartir: {e}")
