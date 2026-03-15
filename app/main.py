from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import rutas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rutas.router)

#python -m venv venv
# .\venv\Scripts\activate
# uvicorn app.main:app --reload
#deactivate
#pip freeze > requirements.txt


# Crear entorno virtual
# python -m venv venv

# Activar entorno virtual
# Windows: venv\Scripts\activate

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