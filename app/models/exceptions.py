from fastapi import Request #Entrega URL
from fastapi.exceptions import RequestValidationError #Entrega mensaje de error
from fastapi.responses import JSONResponse #Preparar la respuesta

MENSAJES_ERROR = {
    # --- USUARIOS ---
    "crearUsuario": {
        "correo": {
            "string_pattern_mismatch": "El correo debe de contener '@utsjr.edu.mx'",
            "string_too_short": "El correo debe tener al menos 10 caracteres",
            "string_too_long": "El correo no debe exceder los 30 caracteres",
            "missing": "El correo es requerido"
        },
        "nombres": {
            "string_too_long": "El nombre no debe exceder los 30 caracteres",
            "missing": "El nombre es requerido"
        },
        "apellidos": {
            "string_too_long": "Los apellidos no deben exceder los 30 caracteres",
            "missing": "Los apellidos son requeridos"
        },
        "contraseña": {
            "missing": "La contraseña es requerida"
        },
        "categoria": {
            "string_too_long": "La categoría no debe exceder los 15 caracteres",
            "missing": "La categoría es requerida"
        },
        "cuatrimestre": {
            "less_than_equal": "El cuatrimestre debe ser igual o menor que 11",
            "greater_than_equal": "El cuatrimestre debe ser igual o mayor que 1",
            "missing": "El cuatrimestre es requerido"
        },
        "plantel": {
            "string_too_long": "El plantel no debe exceder los 10 caracteres",
            "missing": "El plantel es requerido"
        }
    },
    "actualizarUsuario": {
        "nombres": {
            "string_too_long": "El nombre no debe exceder los 30 caracteres"
        },
        "apellidos": {
            "string_too_long": "Los apellidos no deben exceder los 30 caracteres"
        },
        "categoria": {
            "string_too_long": "La categoría no debe exceder los 15 caracteres"
        },
        "cuatrimestre": {
            "less_than_equal": "El cuatrimestre debe ser igual o menor que 11",
            "greater_than_equal": "El cuatrimestre debe ser igual o mayor que 1"
        },
        "plantel": {
            "string_too_long": "El plantel no debe exceder los 10 caracteres"
        }
    },
    "IniciarSesion": {
        "correo": {
            "missing": "El correo es requerido"
        },
        "contraseña": {
            "missing": "La contraseña es requerida"
        }
    },
    
    # --- ASESORES ---
    "crearAsesor": {
        "id_usuario2": {
            "greater_than_equal": "ID de usuario inválido",
            "missing": "El ID de usuario es requerido"
        },
        "carrera": {
            "string_too_long": "La carrera no debe exceder los 150 caracteres",
            "missing": "La carrera es requerida"
        },
        "disponible": {
            "missing": "El campo disponible es requerido",
            "bool_parsing": "El campo disponible debe ser un booleano"
        },
        "categoria": {
            "string_too_long": "La categoría no debe exceder los 15 caracteres",
            "missing": "La categoría es requerida"
        },
        "contacto": {
            "string_too_long": "El contacto no debe exceder los 30 caracteres",
            "missing": "El contacto es requerido"
        }
    },
    "actualizarAsesor": {
        "carrera": {
            "string_too_long": "La carrera no debe exceder los 150 caracteres"
        },
        "categoria": {
            "string_too_long": "La categoría no debe exceder los 15 caracteres"
        },
        "contacto": {
            "string_too_long": "El contacto no debe exceder los 30 caracteres"
        }
    },

    # --- MATERIAS ---
    "crearMateria": {
        "nombre": {
            "string_too_short": "El nombre de la materia es requerido",
            "missing": "El nombre de la materia es requerido"
        },
        "carrera": {
            "string_too_short": "La carrera es requerida",
            "missing": "La carrera es requerida"
        },
        "cuatrimestre": {
            "greater_than_equal": "El cuatrimestre debe ser igual o mayor que 1",
            "missing": "El cuatrimestre es requerido"
        }
    },
    "actualizarMateria": {
        "nombre": {
            "string_too_short": "El nombre de la materia no puede estar vacío"
        },
        "carrera": {
            "string_too_short": "La carrera no puede estar vacía"
        },
        "cuatrimestre": {
             "greater_than_equal": "El cuatrimestre debe ser igual o mayor que 1"
        }
    },

    # --- DISPONIBILIDAD ---
    "crearDisponibilidad": {
        "id_horario": {
             "greater_than_equal": "ID de horario inválido (min 1000)",
             "missing": "ID de horario es requerido"
        },
        "id_asesor1": {
             "greater_than_equal": "ID de asesor inválido (min 1000)",
             "missing": "ID de asesor es requerido"
        },
        "dia": {
            "date_from_datetime_parsing": "Formato de fecha inválido",
            "missing": "El día es requerido"
        },
        "hora_inicio": {
            "time_parsing": "Formato de hora inválido",
            "missing": "Hora de inicio es requerida",
            "value_error": "Error en hora inicio (bloques de 30 min)"
        },
        "hora_fin": {
            "time_parsing": "Formato de hora inválido",
            "missing": "Hora de fin es requerida",
            "value_error": "Hora fin inválida (debe ser mayor a inicio o bloques de 30 min)"
        }
    },
    
    # --- ASESORIA ---
    "crearAsesoria": {
         "tema": {
             "missing": "El tema es requerido"
         },
         "detalles": {
             "missing": "Los detalles son requeridos"
         }
    }
}

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors=[] #SE prepara una lista para almacenar todos los errores
    ruta_obj = request.scope.get("route") #Entrega la ruta completa
    ruta_name = getattr(ruta_obj, "name", "") #Entrega solo el atributo name y si no lo encuentra regresa None
    print(f"Ruta: {ruta_name}")
    print(f"Errores: {exc.errors()}")
    
    for error in exc.errors():
        parametro = error["loc"][-1] 
        tipo = error["type"]
        
        ruta_dic = MENSAJES_ERROR.get(ruta_name, {})
        parametro_dicc = ruta_dic.get(parametro, {})
        
        # Fallbacks: 
        # 1. Custom message for specific error type
        # 2. Generic default for that parameter if we have the param key but not the type key (not implemented here per se, but useful concept)
        # 3. Generic "Error en parámetro X"
        
        mensaje = parametro_dicc.get(tipo, f"Error en el parámetro '{parametro}': {tipo}")
        
        # If we didn't find a custom message in the map, we use the default Pydantic msg or our fallback above
        # The user seems to want custom messages.
        
        errors.append({
            "parametro": parametro,
            "mensaje": mensaje,
            "tipo_error": tipo
        })

    return JSONResponse(
        status_code=422,
        content={
            "detalles": errors
        }
    )