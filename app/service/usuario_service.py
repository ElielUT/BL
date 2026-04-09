from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from app.service.encryptar import cifrar
from postgrest import CountMethod

def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_usuario)

def _table2():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_asesor)

def _table3():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_alumno)

def inicio(correo:str):
    try:
        res = _table().select("id_usuario, correo, contraseña, categoria").eq("correo", str(correo)).execute()
        if res.data:
            return res.data[0]
        else:
            raise HTTPException(status_code=404, detail="Error al encontrar el usuario")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recuperar usuario {e}")
    
def crearUsuario(datos:dict):
    try:
        if not datos:
            raise HTTPException(status_code=404, detail="Datos inexistentes")
        
        cnc = datos.get("contraseña", "")

        sb = get_supabase()
        
        if "contraseña" in datos:
            cc = cifrar(cnc)
            datos["contraseña"] = cc.decode()

        try:
            response = sb.auth.sign_up({
                "email": datos["correo"], 
                "password": cnc
            })
        except Exception as sup_e:
            raise HTTPException(status_code=400, detail=f"Supabase deleygó un error durante el registro: {str(sup_e)}")


        ext = _table().select(count=CountMethod.exact).eq("correo", str(datos["correo"])).execute()
        if ext.data:
            raise HTTPException(status_code=404, detail="Correo ya registrado")
            
        datos = jsonable_encoder(datos)
        res = _table().insert(datos).execute()
        
        if response.user:
            return {
                "status": "success", 
                "message": "Revisa tu correo institucional para verificar tu cuenta.",
                "data": res.data[0] if res.data else None
            }
        else:
            return res.data[0] if res.data else None
    except HTTPException as http_e:
        raise http_e
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
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {e}")
    
def eliminarUsuario(id:int):
    try:
        if not id:
            raise HTTPException(status_code=404, detail="ID faltante")
            
        # 1. Obtener correo antes de borrar localmente
        res_correo = _table().select("correo").eq("id_usuario", int(id)).execute()
        if not res_correo.data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        correo_usuario = res_correo.data[0].get("correo")

        # 2. Borrar localmente
        res = _table().delete().eq("id_usuario", int(id)).execute()
        
        # 3. Eliminar cuenta de auth.users si existe correo
        if correo_usuario:
            sb = get_supabase()
            page = 1
            user_uuid = None
            
            # Buscar iterativamente por páginas a través de los usuarios de Auth
            while True:
                user_list = sb.auth.admin.list_users(page=page, per_page=100)
                # Si la librería de Supabase devuelve una clase con .users o una lista directa
                users_array = getattr(user_list, 'users', user_list) 
                
                if not users_array or len(users_array) == 0:
                    break
                    
                for u in users_array:
                    # 'u' puede ser dict o model dependiendo de tu versión de gotrue
                    if isinstance(u, dict) and u.get("email") == correo_usuario:
                        user_uuid = u.get("id")
                        break
                    elif hasattr(u, "email") and u.email == correo_usuario:
                        user_uuid = u.id
                        break
                        
                if user_uuid or len(users_array) < 100:
                    break
                page += 1
                
            if user_uuid:
                sb.auth.admin.delete_user(user_uuid)

        return {"items": res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el usuario {e}")

def buscarUsuarios(correo:str):
    try:
        res = _table().select("*").eq("correo", correo).execute()
        return {"item":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar usuarios {e}")

def listarUsuarios():
    try:
        res = _table().select("*").execute()
        return {"items":res.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar usuarios {e}")

def buscarUsuarioID(id:int):
    try:
        res = _table().select("*").eq("id_usuario", int(id)).execute()
        if not res.data:
            return {"item": None, "carrera": None}
            
        usuario = res.data[0]
        carrera_data = None
        
        if usuario.get("categoria") == "asesor":
            res2 = _table2().select("carrera").eq("id_usuario2", int(id)).execute()
            if res2.data:
                carrera_data = res2.data[0]
        elif usuario.get("categoria") == "asesorado":
            res2 = _table3().select("carrera").eq("id_usuario1", int(id)).execute()
            if res2.data:
                carrera_data = res2.data[0]
                
        return {"item": usuario, "carrera": carrera_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar usuario {e}")

def cantidadUsuarios():
    try:
        total = _table().select("*", count=CountMethod.exact).execute()
        asesorados = _table().select("*", count=CountMethod.exact).eq("categoria", "asesorado").execute()
        asesores = _table().select("*", count=CountMethod.exact).eq("categoria", "asesor").execute()
        administradores = _table().select("*", count=CountMethod.exact).eq("categoria", "admin").execute()
        return {"Total":total.count, "Asesorados":asesorados.count, "Asesores":asesores.count, "Administradores":administradores.count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al contar usuarios {e}")

def cambiarContraseña(id:int, datos:dict):
    try:
        if not datos or not id:
            raise HTTPException(status_code=404, detail="Datos incompletos")
        
        sb = get_supabase()

        if "contraseña" in datos:
            cnc = datos["contraseña"]
            cc = cifrar(cnc)
            datos["contraseña"] = cc.decode() if isinstance(cc, bytes) else cc
            
            # 1. Obtener correo
            res_correo = _table().select("correo").eq("id_usuario", int(id)).execute()
            if res_correo.data:
                correo_usuario = res_correo.data[0].get("correo")
                
                # 2. Buscar uuid en auth
                page = 1
                user_uuid = None
                while True:
                    user_list = sb.auth.admin.list_users(page=page, per_page=100)
                    users_array = getattr(user_list, 'users', user_list) 
                    
                    if not users_array or len(users_array) == 0:
                        break
                        
                    for u in users_array:
                        if isinstance(u, dict) and u.get("email") == correo_usuario:
                            user_uuid = u.get("id")
                            break
                        elif hasattr(u, "email") and u.email == correo_usuario:
                            user_uuid = u.id
                            break
                            
                    if user_uuid or len(users_array) < 100:
                        break
                    page += 1
                    
                # 3. Actualizar password en Supabase Auth
                if user_uuid:
                    try:
                        sb.auth.admin.update_user_by_id(user_uuid, {"password": cnc})
                    except TypeError:
                        # Fallback for some gotrue versions taking attributes as kwarg
                        sb.auth.admin.update_user_by_id(uid=user_uuid, attributes={"password": cnc})

        datos = jsonable_encoder(datos)
        res = _table().update(datos).eq("id_usuario", int(id)).execute()
        return {"items":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar usuario: {e}")