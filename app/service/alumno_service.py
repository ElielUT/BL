from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
# Importamos la búsqueda de usuario para validar que el alumno exista como usuario primero
from app.service.usuario_service import buscarUsuarioID

def _table():
    sb = get_supabase()
    # Asegúrate de tener 'supabase_alumno' definido en tu config, 
    # o puedes usar el string directo "alumno"
    return sb.schema(config.supabase_schema).table("alumno")

def crearAlumno(data: dict):
    try:
        if not data:
            raise HTTPException(status_code=400, detail="Datos incompletos")
        
        # Validamos que el usuario asociado realmente exista
        res_usuario = buscarUsuarioID(data["id_usuario1"])
        if not res_usuario:
            raise HTTPException(status_code=404, detail="El ID de usuario proporcionado no existe")
        
        data = jsonable_encoder(data)
        res = _table().insert(data).execute()
        return res.data[0] if res.data else None
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el Alumno: {e}")

def actualizarAlumno(id: int, datos: dict):
    try:
        if not datos or not id:
            raise HTTPException(status_code=400, detail="ID o datos faltantes")
        
        datos = jsonable_encoder(datos)
        # Filtramos por id_alumno que es la PK en tu diagrama
        res = _table().update(datos).eq("id_alumno", int(id)).execute()
        
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el Alumno: {e}")

def eliminarAlumno(id: int):
    try:
        if not id:
            raise HTTPException(status_code=400, detail="ID no proporcionado")
            
        res = _table().delete().eq("id_alumno", int(id)).execute()
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el Alumno: {e}")

def listarAlumnos():
    try:
        res = _table().select("*").execute()
        return {"items": res.data if res.data else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar los Alumnos: {e}")

def buscarAlumnoPorID(id: int):
    try:
        if not id:
            raise HTTPException(status_code=400, detail="ID requerido")
            
        res = _table().select("*").eq("id_alumno", int(id)).execute()
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el Alumno: {e}")