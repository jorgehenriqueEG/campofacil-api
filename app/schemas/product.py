from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal
    stock: int = 0


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    stock: int | None = None


class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock: int
    created_at: datetime

    model_config = {"from_attributes": True}
