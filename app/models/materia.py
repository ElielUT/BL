from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.supabase_client import Base # Usamos la base que ya tienen en centro

class Materia(Base):
    __tablename__ = "materia"
    id_materia = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    carrera = Column(String)
    cuatrimestre = Column(Integer)

class Impartir(Base):
    __tablename__ = "impartir"
    id_impartir = Column(Integer, primary_key=True, index=True)
    id_materia2 = Column(Integer, ForeignKey("materia.id_materia"))
    id_asesor2 = Column(Integer, ForeignKey("asesor.id_asesor"))
