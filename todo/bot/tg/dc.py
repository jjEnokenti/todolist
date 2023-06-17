from dataclasses import dataclass
from typing import List

from aiogram.types import (
    Message,
    Update
)
from marshmallow import EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[Update]

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE
