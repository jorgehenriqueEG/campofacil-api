from fastapi import APIRouter

router = APIRouter()

@router.get("/clientes")
def listar_clientes():
    return [
        {"id": 1, "nome": "Cliente 1"},
        {"id": 2, "nome": "Cliente 2"}
    ]