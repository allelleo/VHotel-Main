import datetime

from core import settings
from fastapi import APIRouter, Request
from room import models, schemas, service

room = APIRouter()


class FakeAdmin:
    is_admin = True


@room.post("/create/room/dev")
async def create_room_dev(
    room_type: str,
    capasity: int,
    desc: str,
    price: int,
    service: list[str],
    img: list[str],
):
    room = models.Room(
        room_type=room_type, capasity=capasity, description=desc, price=price
    )
    await room.save()

    for srv in service:
        if await models.RoomService.exists(title=srv):
            s = await models.RoomService.get(title=srv)
            await room.services.add(s)
            await room.save()
        else:
            s = await models.RoomService.create(title=srv)
            await room.services.add(s)
            await room.save()

    for im in img:
        if await models.RoomImage.exists(src=im):
            i = await models.RoomImage.get(src=im)
            await room.images.add(i)
            await room.save()
        else:
            i = await models.RoomImage.create(src=im)
            await room.images.add(i)
            await room.save()

    return room.id


@room.post("/create/reserv/dev")
async def create_reservation_dev(
    date_in: datetime.date,
    date_out: datetime.date,
    car_place: int,
    guest_count: int,
    email: str,
    phone: str,
    first_name: str,
    last_name: str,
    room_id: int,
    state: str,
):
    print(guest_count)
    r = await models.Reservation.create(
        date_in=date_in,
        date_out=date_out,
        car_place=car_place,
        guests_count=guest_count,
        email=email,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        state=state,
    )
    room = await models.Room.get(id=room_id)
    await room.reservation.add(r)
    await room.save()
    return r.id


@room.get("/all")
async def get_all_rooms(r: Request):
    return await service.RoomService.get_all_rooms()


@room.get("/unique")
async def get_room_unique_type(r: Request):
    return await service.RoomService.get_room_unique_type()


@room.get("/get")
async def get_room_by_id(r: Request, room_id: int):
    return await service.RoomService.get_room_by_id(room_id)


@room.post("/reserv")
async def reservation_room(r: Request, data: schemas.ReservationRequest):
    return await service.RoomService.reservation_room(data)


@room.get("/admin/info")
async def get_rooms_all_info(r: Request):
    return await service.AdminLogic.get_rooms_all_info(FakeAdmin())


@room.get("/admin/room/status")
async def change_room_status(r: Request, room_id: int, status: bool):
    return await service.AdminLogic.change_room_status(
        user=FakeAdmin(), room_id=room_id, status=status
    )


@room.get("/admin/room/price")
async def change_room_price(r: Request, room_id: int, price: int):
    return await service.AdminLogic.change_room_price(
        user=FakeAdmin(), room_id=room_id, price=price
    )


@room.get("/admin/reservation/accept")
async def reservation_accept(r: Request, reservation_id: int):
    return await service.AdminLogic.reservation_accept(
        user=FakeAdmin(), reservation_id=reservation_id
    )


@room.get("/admin/reservation/change")
async def reservation_change_status(
    r: Request, reservation_id: int, status: settings.RESRVATION_STATES_LITERAL
):
    return await service.AdminLogic.reservation_change_status(
        user=FakeAdmin(), reservation_id=reservation_id, status=status
    )


@room.get("/add/rooms/json")
async def add_roms_from_json_dev_func():
    import json

    data = json.loads(open("core/rooms.json", encoding="utf-8").read())["rooms"]

    for room in data:
        srv = []
        imgs = []
        for service in room["services"]:
            if await models.RoomService.exists(title=service["title"]):
                srv.append(await models.RoomService.get(title=service["title"]))
            else:
                srv.append(await models.RoomService.create(title=service["title"]))
        for img in room["images"]:
            if await models.RoomImage.exists(src=img["src"]):
                imgs.append(await models.RoomImage.get(src=img["src"]))
            else:
                imgs.append(await models.RoomImage.create(src=img["src"]))
        room = models.Room(
            room_type=room["room_type"],
            capasity=room["capasity"],
            description=room["description"],
            price=room["price"],
        )
        await room.save()
        for i in srv:
            await room.services.add(i)
            await room.save()
        for i in imgs:
            await room.images.add(i)
            await room.save()
        print("OK")
