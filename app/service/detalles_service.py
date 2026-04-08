from fastapi import HTTPException
from app.core.supabase_client import get_supabase
from app.core.config import config
from datetime import datetime

def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_toma)

def _calcular_duracion(hora_in: str, hora_fin: str):
    try:
        fmt = "%H:%M:%S"
        t1 = datetime.strptime(hora_in, fmt)
        t2 = datetime.strptime(hora_fin, fmt)
        delta = (t2 - t1).seconds // 60
        return delta if delta > 0 else None
    except Exception:
        return None

def _determinar_estado(toma: dict) -> str:
    return toma.get("estado") or "pendiente"

def obtener_detalles_asesoria(id_asesoria: int) -> dict:
    try:
        res = _table().select(
            "*, asesoria(*, materia(*)), asesor(*, usuario(*)), alumno(*, usuario(*))"
        ).eq("id_asesoria1", id_asesoria).execute()

        if not res.data or len(res.data) == 0:
            raise HTTPException(status_code=404, detail="Sesión no encontrada")

        t = res.data[0]

        alumno_u = (t.get("alumno") or {}).get("usuario") or {}
        nombre_asesorado = f"{alumno_u.get('nombres', '')} {alumno_u.get('apellidos', '')}".strip() or "Sin nombre"

        asesor_u = (t.get("asesor") or {}).get("usuario") or {}
        nombre_asesor = f"{asesor_u.get('nombres', '')} {asesor_u.get('apellidos', '')}".strip() or "Sin nombre"

        asesoria    = t.get("asesoria") or {}
        materia_obj = asesoria.get("materia") or {}
        materia     = materia_obj.get("nombre") or "Sin materia"
        tema        = asesoria.get("tema") or "Sin tema"
        modalidad   = asesoria.get("modalidad") or "virtual"

        hora_in  = str(t.get("hora_in")  or "")[:5] or None
        hora_fin = str(t.get("hora_fin") or "")[:5] or None
        duracion = None
        if t.get("hora_in") and t.get("hora_fin"):
            duracion = _calcular_duracion(str(t["hora_in"]), str(t["hora_fin"]))

        return {
            "id_asesoria":      id_asesoria,
            "id_asesor3":       t.get("id_asesor3"),
            "id_alumno1":       t.get("id_alumno1"),
            "materia":          materia,
            "tema":             tema,
            "modalidad":        modalidad,
            "nombre_asesorado": nombre_asesorado,
            "nombre_asesor":    nombre_asesor,
            "lugar":            "Reunión virtual" if modalidad == "virtual" else "Presencial",
            "contacto":         (t.get("asesor") or {}).get("contacto") or None,
            "fecha":            str(t.get("fecha")) if t.get("fecha") else None,
            "hora_in":          hora_in,
            "hora_fin":         hora_fin,
            "duracion_min":     duracion,
            "fecha_solicitud":  str(t.get("fecha_solicitud")) if t.get("fecha_solicitud") else None,
            "meet_link":        t.get("meet_link"),
            "calificacion":     t.get("calificacion"),
            "estado":           _determinar_estado(t),
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener detalles: {e}")

def guardar_meet_link(id_asesor3: int, id_asesoria1: int, id_alumno1: int, meet_link: str) -> dict:
    try:
        res = _table().update({"meet_link": meet_link}).eq("id_asesor3", id_asesor3).eq("id_asesoria1", id_asesoria1).eq("id_alumno1", id_alumno1).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Toma no encontrada")
        return {"meet_link": meet_link, "id_asesoria1": id_asesoria1}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar meet_link: {e}")