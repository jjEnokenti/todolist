from dataclasses import (
    dataclass,
    field,
)
from typing import List

import marshmallow_dataclass
from marshmallow import EXCLUDE


@dataclass
class BaseSchema:
    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat(BaseSchema):
    id: int
    first_name: str | None
    username: str | None


@dataclass
class User(BaseSchema):
    id: int
    is_bot: bool
    first_name: str | None
    username: str | None


@dataclass
class Message(BaseSchema):
    message_id: int
    from_user: User = field(metadata={'data_key': 'from'})
    chat: Chat
    text: str


@dataclass
class Update(BaseSchema):
    update_id: int
    message: Message | None
    edited_message: Message | None


@dataclass
class GetUpdatesResponse(BaseSchema):
    ok: bool
    result: List[Update]


@dataclass
class SendMessageResponse(BaseSchema):
    ok: bool
    result: Message


get_updates_schema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
send_message_schema = marshmallow_dataclass.class_schema(SendMessageResponse)
