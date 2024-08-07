import datetime

from tortoise.fields import (
    BinaryField,
    BooleanField,
    CharField,
    DateField,
    DatetimeField,
    IntField,
    ManyToManyField,
    TextField,
)
from tortoise.models import Model


class Action(Model):
    id = IntField(pk=True)
    time_created = DatetimeField(auto_now_add=True)
    time_updated = DatetimeField(auto_now=True)

    content: str = CharField(max_length=250)

    async def json(self):
        return {
            "id": self.id,
            "content": self.content,
            "time_created": self.time_created,
        }
