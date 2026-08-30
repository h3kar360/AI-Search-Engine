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

    # One-to-Many Relationship
    chats: Mapped[list["Chats"]] = relationship(
        "Chats",
        back_populates="conversations",
        cascade="all, delete-orphan"
    )

class Chats(Base):
    __tablename__ = "chats"
    
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

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False
    )

    conversations: Mapped["Conversations"] = relationship(
        "Conversations", 
        back_populates="chats"
    )