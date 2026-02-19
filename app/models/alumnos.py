from pydantic import BaseModel, Field, ConfigDict

class CrearAlumno(BaseModel):
    model_config = ConfigDict(title="Crear Alumno")
    
    # Usamos ge=1000 si quieres mantener la regla de los 4 dígitos
    id_usuario1: int = Field(ge=1, le=9999) 
    carrera: str = Field(max_length=150)
    contacto: str = Field(max_length=30)
    salon: str = Field(max_length=10)

class ActualizarAlumno(BaseModel):
    model_config = ConfigDict(title="Actualizar Alumno")
    
    # Todos los campos son opcionales para actualizaciones parciales
    carrera: str | None = Field(None, max_length=150)
    contacto: str | None = Field(None, max_length=30)
    salon: str | None = Field(None, max_length=10)

class RecuperarAlumno(BaseModel):
    # Este modelo es el que devuelve la base de datos (incluye el ID)
    id_alumno: int
    id_usuario1: int
    carrera: str
    contacto: str
    salon: str

class ListaAlumnos(BaseModel):
    items: list[RecuperarAlumno]

class SoloAlumno(BaseModel):
    item: RecuperarAlumno