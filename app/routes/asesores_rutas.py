#FastAPI y Supabase
from fastapi import APIRouter,HTTPException

from app.models.asesor import CrearAsesor, ActualizarAsesor, ListaAsesor, SoloAsesor 

from app.service.asesor_service import eliminarAsesor, crearAsesor, actualizarAsesor, listarAsesores, buscarAsesorPorMateria, buscarAsesorPorAsesorNombre, buscarAsesorPorAsesorID, eliminarAsesorForaneo, actualizarAsesorForaneo

router = APIRouter(prefix="/asesores", tags=["Asesores"])

"""
Routes de Asesores
"""
@router.post("/crearAsesor", response_model=CrearAsesor, name="crearAsesor")
def crear_Asesor(body:CrearAsesor):
    return crearAsesor(body.model_dump())

@router.get("/eliminarAsesor/{id_asesor}", name="eliminarAsesor")
def eliminar_Asesor(id_asesor:int):
    return eliminarAsesor(id_asesor)

@router.put("/actualizarAsesor/{id_asesor}", response_model=ActualizarAsesor, name="actualizarAsesor")
def actualizar_Asesor(id_asesor:int, body:ActualizarAsesor):
    return actualizarAsesor(id_asesor, body.model_dump(exclude_none=True))

@router.get("/listarAsesores", response_model=ListaAsesor, name="listarAsesores")
def listar_Asesores():
    return listarAsesores()

@router.get("/buscarAsesorMateria/{materia}", response_model=ListaAsesor, name="buscarAsesorMateria")
def buscar_Asesor(materia:str):
    return buscarAsesorPorMateria(materia)

@router.get("/buscarAsesorUsuario/{usuario}", response_model=ListaAsesor, name="buscarAsesorUsuario")
def buscar_AsesorUsuario(usuario:str):
    return buscarAsesorPorAsesorNombre(usuario)

@router.get("/buscarAsesorID/{id_asesor}", response_model=SoloAsesor, name="buscarAsesorID")
def buscar_AsesorID(id_asesor:int):
    return buscarAsesorPorAsesorID(id_asesor)

@router.delete("/eliminarAsesorForaneo/{id_asesor}")
async def borrar_asesor(id_asesor: int):
    res = eliminarAsesorForaneo(id_asesor)
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo eliminar el asesor o no existe")
    return {"message": "Asesor eliminado exitosamente", "id": id_asesor}

@router.put("/actualizarAsesorForaneo/{id_usuario}")
async def actualizar_asesor_foraneo(id_usuario: int, datos: dict):
    res = actualizarAsesorForaneo(id_usuario, datos.get("carrera"), datos.get("categoria"))
    if not res or not res.get("items"):
        raise HTTPException(status_code=404, detail="No se pudo actualizar el asesor o no existe")
    return {"message": "Asesor actualizado exitosamente", "id": id_usuario}