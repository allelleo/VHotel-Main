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


class Reservation(Model):
    date_in: datetime.datetime = DateField()
    date_out: datetime.datetime = DateField()
    car_place: int = IntField()
    guests_count: int = IntField()
    email: str = CharField(max_length=60)
    phone: str = CharField(max_length=30)
    first_name: str = CharField(max_length=60)
    last_name: str = CharField(max_length=60)
    state: str = CharField(max_length=60)

    async def json(self):
        return {
            "id": self.id,
            "date_in": self.date_in,
            "date_out": self.date_out,
            "car_place": self.car_place,
            "guests_count": self.guests_count,
            "email": self.email,
            "phone": self.phone,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "state": self.state,
        }


class RoomImage(Model):
    id = IntField(pk=True)
    time_created = DatetimeField(auto_now_add=True)
    time_updated = DatetimeField(auto_now=True)

    src: str = CharField(max_length=250)

    async def json(self):
        return {"id": self.id, "src": self.src}


class RoomService(Model):
    id = IntField(pk=True)
    time_created = DatetimeField(auto_now_add=True)
    time_updated = DatetimeField(auto_now=True)

    title: str = CharField(max_length=200)

    async def json(self):
        return {"id": self.id, "title": self.title}


class Room(Model):
    id = IntField(pk=True)
    time_created = DatetimeField(auto_now_add=True)
    time_updated = DatetimeField(auto_now=True)

    room_type: str = CharField(max_length=100)
    capasity: int = IntField()
    description: str = CharField(max_length=300)
    price: int = IntField()

    status: str = BooleanField(default=True)  # True = доступен

    images = ManyToManyField("models.RoomImage")
    services = ManyToManyField("models.RoomService")
    reservation = ManyToManyField("models.Reservation")

    async def json(self, include_reservations=False):
        images = [await img.json() for img in await self.images.all()]
        services = [await srv.json() for srv in await self.services.all()]
        if not include_reservations:
            return {
                "id": self.id,
                "room_type": self.room_type,
                "capasity": self.capasity,
                "description": self.description,
                "price": self.price,
                "status": self.status,
                "images": images,
                "services": services,
            }
        reservations = [await rsrv.json() for rsrv in await self.reservation.all()]
        return {
            "id": self.id,
            "room_type": self.room_type,
            "capasity": self.capasity,
            "description": self.description,
            "price": self.price,
            "status": self.status,
            "images": images,
            "services": services,
            "reservations": reservations,
        }
