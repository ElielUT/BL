from fastapi import FastAPI
from app.routes import rutas

app = FastAPI()

app.include_router(rutas.router)

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