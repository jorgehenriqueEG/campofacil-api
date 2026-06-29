from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
