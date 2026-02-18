from fastapi import Request #Entrega URL
from fastapi.exceptions import RequestValidationError #Entrega mensaje de error
from fastapi.responses import JSONResponse #Preparar la respuesta

MENSAJES_ERROR = {
    "crearUsuario":{
        "cuatrimestre":{
            "less_than_equal":"El cuatrimestre debe ser igual o menor que 11",
        },
        "correo":{
            "string_pattern_mismatch":"El correo debe de contener '@utsjr.edu.mx'"
        }
    }
}

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors=[] #SE prepara una lista para almacenar todos los errores
    ruta_obj = request.scope.get("route") #Entrega la ruta completa
    ruta_name = getattr(ruta_obj, "name", "") #Entrega solo el atributo name y si no lo encuentra regresa None
    print(ruta_name)
    print(exc.errors())
    for error in exc.errors():
        parametro = error["loc"][-1]
        tipo = error["type"]
        ruta_dic = MENSAJES_ERROR.get(ruta_name, {})
        parametro_dicc = ruta_dic.get(parametro, {})
        mensaje_dicc = parametro_dicc.get(tipo, f"Error en el parámetro {parametro}")
        errors.append(mensaje_dicc)

        print(tipo)

    return JSONResponse(
        status_code=422,
        content={
            "detalles":errors
        }
    )