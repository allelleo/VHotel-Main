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


class News(Model):
    id = IntField(pk=True)
    time_created = DatetimeField(auto_now_add=True)
    time_updated = DatetimeField(auto_now=True)

    title: str = CharField(max_length=250)
    image: str = CharField(max_length=250)
    link: str = CharField(max_length=250)

    async def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image,
            "link": self.link,
            "time_created": self.time_created,
        }
