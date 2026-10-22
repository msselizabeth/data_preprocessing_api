from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass


class ApiClient(Base):
    __tablename__ = "api_clients"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True, autoincrement=True)
    api_key_hash: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)