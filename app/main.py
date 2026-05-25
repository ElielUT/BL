# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from app.routes import rutas, alumnos_rutas, asesores_rutas, asesoria_rutas, disponibilidad_rutas, materias_rutas, toma_rutas, usuarios_rutas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rutas.router)
app.include_router(alumnos_rutas.router)
app.include_router(asesores_rutas.router)
app.include_router(asesoria_rutas.router)
app.include_router(disponibilidad_rutas.router)
app.include_router(materias_rutas.router)
app.include_router(toma_rutas.router)
app.include_router(usuarios_rutas.router)

#python -m venv venv
# .\venv\Scripts\activate
# uvicorn app.main:app --reload
#deactivate
#pip freeze > requirements.txt


# Crear entorno virtual
# python -m venv venv

# Activar entorno virtual
# Windows: venv\Scripts\activate
# Linux: source venv/bin/activate

# Salir del entorno virtual
# deactivate

# Instalar el framework y servidor
# pip install fastApi uvicorn

# Crear archivo con todas las instalaciones
# pip freeze > requirements.txt

# Instalar lo que está en requirements.txt
# pip install -r requirements.txt

# Ejecutar programa
# uvicorn main:app --reload