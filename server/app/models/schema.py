import uuid

from pydantic import BaseModel, ConfigDict
from typing import Any

# ---General---

class RaiseMessage(BaseModel):
    message: str

# ---Conversation---

class InsertConvo(BaseModel):
    title: str

class ConvoInfoResponse(BaseModel):
    id: uuid.UUID
    title: str

    model_config = ConfigDict(from_attributes=True)

class ConvoChatsResponse(ConvoInfoResponse):
    role: str
    content: str
    sources: list[dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)

# ---Chats---

class SendChat(BaseModel):
    query: str

class SaveChat(BaseModel):
    role: str
    content: str
    sources: list[dict[str, Any]]

class ChatResponse(BaseModel):
    response: str
    sources: list[dict[str, Any]]