from fastapi import FastAPI
from app.routes import rutas

app = FastAPI()

app.include_router(rutas.router)

#python -m venv venv
# .\venv\Scripts\activate
# uvicorn app.main:app --reload
#deactivate
#pip freeze > requirements.txt