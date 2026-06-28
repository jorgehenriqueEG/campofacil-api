from fastapi import FastAPI
from app.routes import clientes

app = FastAPI()

app.include_router(clientes.router)

@app.get("/")
def home():
    return {"msg": "CampoFácil rodando"}