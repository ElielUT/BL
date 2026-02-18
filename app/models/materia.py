from sqlalchemy import Column, Integer, ForeignKey
from centro.supabase_client import Base 

class Impartir(Base):
    __tablename__ = "impartir"

    id_impartir = Column(Integer, primary_key=True, index=True)
    # id_materia2 debe coincidir con el nombre en tu diagrama ERD
    id_materia2 = Column(Integer, ForeignKey("materia.id_materia"), nullable=False)
    # id_asesor2 apunta a la tabla asesor
    id_asesor2 = Column(Integer, ForeignKey("asesor.id_asesor"), nullable=False)
