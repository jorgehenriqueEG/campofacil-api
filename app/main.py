from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.clients import router as clients_router
from routes.products import router as products_router

app = FastAPI(title="Campofacil API")

app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(products_router)
