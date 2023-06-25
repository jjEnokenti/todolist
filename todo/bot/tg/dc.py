from dataclasses import (
    dataclass,
    field,
)
from typing import List

import marshmallow_dataclass
from marshmallow import EXCLUDE


@dataclass
class BaseSchema:
    """Base schema."""
    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat(BaseSchema):
    """Chat schema."""
    id: int
    first_name: str | None
    username: str | None


@dataclass
class User(BaseSchema):
    """User schema."""
    id: int
    is_bot: bool
    first_name: str | None
    username: str | None


@dataclass
class Message(BaseSchema):
    """Message schema."""
    message_id: int
    from_user: User = field(metadata={'data_key': 'from'})
    chat: Chat
    text: str


@dataclass
class Update(BaseSchema):
    """Telegram update schema."""
    update_id: int
    message: Message | None
    edited_message: Message | None


@dataclass
class GetUpdatesResponse(BaseSchema):
    """Updates response schema."""
    ok: bool
    result: List[Update]


@dataclass
class SendMessageResponse(BaseSchema):
    """Send message response schema."""
    ok: bool
    result: Message


get_updates_schema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
send_message_schema = marshmallow_dataclass.class_schema(SendMessageResponse)
