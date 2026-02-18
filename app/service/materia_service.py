from sqlalchemy.orm import Session
from modelos.materia import Materia, Impartir
from modelos.asesor import Asesor # Importante para validar que el asesor existe
from fastapi import HTTPException

def crear_materia_db(db: Session, materia_schema):
    # Validar que no exista el mismo nombre
    existe = db.query(Materia).filter(Materia.nombre == materia_schema.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="Materia ya registrada")
    
    nueva = Materia(**materia_schema.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def asignar_impartir_db(db: Session, impartir_schema):
    # Validar que existan ambos IDs antes de crear la relación
    m_existe = db.query(Materia).filter(Materia.id_materia == impartir_schema.id_materia2).first()
    a_existe = db.query(Asesor).filter(Asesor.id_asesor == impartir_schema.id_asesor2).first()
    
    if not m_existe or not a_existe:
        raise HTTPException(status_code=404, detail="Materia o Asesor no encontrados")
        
    nueva_relacion = Impartir(**impartir_schema.model_dump())
    db.add(nueva_relacion)
    db.commit()
    db.refresh(nueva_relacion)
    return nueva_relacion
