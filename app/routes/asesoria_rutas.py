#FastAPI y Supabase
from fastapi import APIRouter

from app.models.asesoria import ActualizarAsesoria, CrearAsesoria, ListaAsesoria, SoloAsesoria

from app.service.asesoria_service import crearAsesoria, eliminarAsesoria, actualizarAsesoria

router = APIRouter(prefix="/asesoria", tags=["asesoria"])

"""
Routes de Asesoria
"""
@router.post("/crearAsesoria", name="crearAsesoria")
def crear_Asesoria(body:CrearAsesoria):
    return crearAsesoria(body.model_dump())

@router.get("/eliminarAsesoria/{id_asesoria}", name="eliminarAsesoria")
def eliminar_Asesoria(id_asesoria:int):
    return eliminarAsesoria(id_asesoria)

@router.put("/actualizarAsesoria/{id_asesoria}", response_model=ActualizarAsesoria, name="actualizarAsesoria")
def actualizar_Asesoria(id_asesoria:int, body:ActualizarAsesoria):
    return actualizarAsesoria(id_asesoria, body.model_dump(exclude_none=True))

@router.get("/mostrarAsesoria", name="mostrarAsesoria")
def endpoint_mostrar_Asesoria():
    from app.service.asesoria_service import mostrar_asesoria_supervisar
    return mostrar_asesoria_supervisar()

@router.get("/estadisticas", name="estadisticasAsesoria")
def endpoint_estadisticas_asesoria():
    from app.service.asesoria_service import estadisticas_asesoria_supervisar
    return estadisticas_asesoria_supervisar()
