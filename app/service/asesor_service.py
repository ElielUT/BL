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

def eliminarAsesorForaneo(id:int):
    try:
        if not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        res = _table().delete().eq("id_usuario2", int(id)).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el Asesor {e}")

def actualizarAsesorForaneo(id:int, carrera:str):
    try:
        if not id or not carrera:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        res = _table().update({"carrera": carrera}).eq("id_usuario2", int(id)).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el Asesor {e}")

def listarAsesores():
    try:
        sb = get_supabase()
        res = sb.schema(config.supabase_schema).table(config.supabase_asesor)\
            .select("*, usuario(*)") \
            .execute()
        return {"items": res.data if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar los Asesores {e}")

def buscarAsesorPorMateria(materia:str):
    try:
        if not materia:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        
        sb = get_supabase()
        
        # Paso 1: Buscar la materia por nombre
        resMat = sb.schema(config.supabase_schema).table(config.supabase_materia)\
            .select("*") \
            .eq("nombre", materia)\
            .execute()
        
        print(f"Paso 1 - Materia encontrada: {resMat.data}")
        
        if not resMat.data:
            return {"items": []}
        
        id_materia = resMat.data[0]["id_materia"]
        
        # Paso 2: Buscar en imparte los asesores de esa materia
        resImp = sb.schema(config.supabase_schema).table(config.supabase_imparte)\
            .select("id_asesor2") \
            .eq("id_materia2", id_materia)\
            .execute()
        
        print(f"Paso 2 - Imparte encontrado: {resImp.data}")
        
        if not resImp.data:
            return {"items": []}
        
        # Paso 3: Obtener los IDs de los asesores
        ids_asesores = [item["id_asesor2"] for item in resImp.data]
        print(f"Paso 3 - IDs de asesores: {ids_asesores}")
        
        # Paso 4: Buscar cada asesor y su usuario
        asesores_con_usuario = []
        for id_asesor in ids_asesores:
            # Buscar asesor
            resAsesor = sb.schema(config.supabase_schema).table(config.supabase_asesor)\
                .select("*") \
                .eq("id_asesor", id_asesor)\
                .execute()
            
            print(f"Paso 4a - Asesor encontrado: {resAsesor.data}")
            
            if resAsesor.data:
                asesor = resAsesor.data[0]
                
                print(f"Buscando usuario con id_usuario: {asesor['id_usuario2']}")
                
                # Buscar usuario asociado
                resUsuario = sb.schema(config.supabase_schema).table(config.supabase_usuario)\
                    .select("nombres, apellidos, correo") \
                    .eq("id_usuario", asesor["id_usuario2"])\
                    .execute()
                
                print(f"Paso 4b - Usuario encontrado: {resUsuario.data}")
                
                if resUsuario.data:
                    usuario = resUsuario.data[0]
                    asesor["nombres"] = usuario["nombres"]
                    asesor["apellidos"] = usuario["apellidos"]
                    asesor["correo_usuario"] = usuario["correo"]
                
                asesores_con_usuario.append(asesor)
        
        print(f"Resultado final: {asesores_con_usuario}")
        return {"items": asesores_con_usuario}
        
    except Exception as e:
        print(f"Error detallado: {e}")
        raise HTTPException(status_code=500, detail=f"Error al buscar el Asesor: {str(e)}")

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
        sb = get_supabase()
        res = sb.schema(config.supabase_schema).table(config.supabase_asesor)\
            .select("*, usuario(*)") \
            .eq("id_asesor", int(id))\
            .execute()
        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar el Asesor {e}")