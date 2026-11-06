from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import  Mapped, mapped_column
from .api_clients_model import Base
from datetime import datetime, timezone


class JsonMapping(Base):
    __tablename__ = "json_mappings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    mapping: Mapped[dict[str, str]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc),nullable=False)

    client_id: Mapped[int] = mapped_column(ForeignKey("api_clients.id"), nullable=False)