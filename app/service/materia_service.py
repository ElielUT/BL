from sqlalchemy.orm import Session
from modelos.materia import Impartir, Materia
from modelos.asesor import Asesor # Asegúrate de importar el modelo de asesor
from fastapi import HTTPException

def servicio_asignar_materia_asesor(db: Session, datos_impartir):
    # 1. Validar que la materia existe
    if not db.query(Materia).filter(Materia.id_materia == datos_impartir.id_materia2).first():
        raise HTTPException(status_code=404, detail="La materia no existe")

    # 2. Validar que el asesor existe
    if not db.query(Asesor).filter(Asesor.id_asesor == datos_impartir.id_asesor2).first():
        raise HTTPException(status_code=404, detail="El asesor no existe")

    # 3. Evitar duplicados (que el mismo asesor imparta la misma materia dos veces)
    existe = db.query(Impartir).filter(
        Impartir.id_materia2 == datos_impartir.id_materia2,
        Impartir.id_asesor2 == datos_impartir.id_asesor2
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Esta asignación ya existe")

    nueva_asignacion = Impartir(**datos_impartir.model_dump())
    db.add(nueva_asignacion)
    db.commit()
    db.refresh(nueva_asignacion)
    return nueva_asignacion
