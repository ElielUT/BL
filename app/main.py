from fastapi import FastAPI
from app.routes import rutas

app = FastAPI()

app.include_router(rutas.router)

# .\venv\Scripts\activate
# uvicorn app.main:app --reload
#deactivate