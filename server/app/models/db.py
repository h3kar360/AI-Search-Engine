import uuid

from datetime import datetime

from app.db.session import Base
from sqlalchemy import String, UUID, DateTime, text, func
from sqlalchemy.orm import Mapped, mapped_column

class Conversations(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    title: Mapped[str | None] = mapped_column(
        String,
        default="Untitled",
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )