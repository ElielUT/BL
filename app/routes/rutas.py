from fastapi import APIRouter, Path, Query

router = APIRouter()

@router.get("/")
def h():
    return {"Inicio": "Inicio"}