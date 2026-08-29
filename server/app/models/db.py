import uuid

from datetime import datetime
from typing import Any

from app.db.session import Base
from sqlalchemy import ForeignKey, String, UUID, DateTime, text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Conversations(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    title: Mapped[str] = mapped_column(
        String,
        default="Untitled",
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    chat_history_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_history.id", ondelete="CASCADE"),
        nullable=False
    )

    chat_history = relationship(
        "ChatHistory", 
        back_populates="conversations"
    )

class ChatHistory(Base):
    __tablename__ = "chat_history"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    role: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    sources: Mapped[list[dict[str, Any]]] = mapped_column(
        JSONB,
        server_default="[]",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    conversations = relationship(
        "Conversations",
        back_populates="chat_history",
        cascade="all, delete-orphan"
    )
