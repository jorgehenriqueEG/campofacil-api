from datetime import datetime
from pydantic import BaseModel, EmailStr


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None


class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


class ClientOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
