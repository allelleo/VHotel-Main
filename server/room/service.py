import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from core import settings
from room import exceptions, models, schemas
from tortoise.expressions import Q as Query
from user import models as user_models


async def check_room_type_exists(room_type: str):
    if not await models.Room.exists(room_type=room_type):
        raise exceptions.RoomTypeNotFound


async def check_dates(date_in: datetime.date, date_out: datetime.date):
    if date_out < date_in or (date_out - date_in).days < 2:
        raise exceptions.DatesFail


class RoomService:
    @staticmethod
    async def get_all_rooms():
        return [await room.json() for room in await models.Room.filter(status=True)]

    @staticmethod
    async def get_room_unique_type():
        types: list[str] = []
        data: list[dict] = []
        for room in await models.Room.filter(status=True):
            if not room.room_type in types:
                data.append(await room.json())
                types.append(room.room_type)
        return data

    @staticmethod
    async def get_room_by_id(room_id: int):
        try:
            room = await models.Room.get(id=room_id)
        except:
            raise exceptions.RoomNotFound
        return await room.json()

    @staticmethod
    async def reservation_create(data: schemas.ReservationRequest, room_id: int):
        reservation = await models.Reservation.create(
            date_in=data.date_in,
            date_out=data.date_out,
            car_place=data.car_place,
            guests_count=data.guest_count,
            email=data.email,
            phone=data.phone,
            first_name=data.first_name,
            last_name=data.last_name,
            state=settings.ReservationState.CREATED.value,
        )
        room = await models.Room.get(id=room_id)
        await room.reservation.add(reservation)
        return True

    @staticmethod
    async def check_car_places(dates: list[datetime.date], places: int):
        if places == 0:
            print("PARKING +")
            return
        filter = [
            Query(state=settings.ReservationState.CREATED.value),
            Query(state=settings.ReservationState.WAIT.value),
            Query(state=settings.ReservationState.COME.value),
        ]
        rooms = await models.Room.filter(status=True)
        car_place_bisy = []
        for room in rooms:
            for date in dates:
                pl = 0
                for reservation in await room.reservation.filter(*filter):
                    if reservation.date_in <= date <= reservation.date_out:
                        pl += 1
                car_place_bisy.append(pl + places)
        if any(
            [True if i > settings.PARKING_PLACES else False for i in car_place_bisy]
        ):
            return False
        return True

        # for reservation

    @staticmethod
    async def reservation_room(data: schemas.ReservationRequest):
        # TODO: check capasity
        # TODO: send email to admin
        await check_dates(data.date_in, data.date_out)
        await check_room_type_exists(data.room_type)

        rooms = await models.Room.filter(
            Query(Query(room_type=data.room_type) & Query(status=True))
        )

        dates = [data.date_in]
        for i in range(1, (data.date_out - data.date_in).days):
            dates.append(data.date_in + datetime.timedelta(days=i))
        dates.append(data.date_out)
        print(dates)
        for room in rooms:
            print(room.id)
            reservations = await room.reservation.filter(
                *[
                    Query(state=settings.ReservationState.CREATED.value)
                    | Query(state=settings.ReservationState.WAIT.value)
                    | Query(state=settings.ReservationState.COME.value)
                ]
            )
            if len(reservations) == 0:
                await RoomService.check_car_places(dates, data.car_place)
                await RoomService.reservation_create(data, room.id)
                return {"status": "ok"}

            approached = True
            for reservation in reservations:

                for date in dates:
                    if reservation.date_in <= date <= reservation.date_out:
                        approached = False

            if approached:
                res = await RoomService.check_car_places(dates, data.car_place)
                await RoomService.reservation_create(data, room.id)
                smtpObj = smtplib.SMTP("smtp.timeweb.ru", 25)
                msg = MIMEText(
                    f"Гость зарезервировал новую комнату\nС {data.date_in} до {data.date_out}",
                    "plain",
                    "utf-8",
                )
                msg["Subject"] = Header("Новая бронь", "utf-8")
                msg["From"] = "support@voskresensky-hotel.ru"
                msg["To"] = "support@voskresensky-hotel.ru"
                smtpObj.starttls()
                smtpObj.login("support@voskresensky-hotel.ru", "xxXX1234")
                smtpObj.sendmail(msg["From"], msg["To"], msg.as_string())
                smtpObj.quit()
                if res == False:
                    return {"status": "ok", "message": "car places"}
                return {"status": "ok"}

        raise exceptions.ReservationFail


async def check_admin(user: user_models.User):
    if not user.is_admin:
        raise exceptions.UserNotAdmin


class AdminLogic:

    @staticmethod
    async def get_rooms_all_info(user: user_models.User):
        await check_admin(user)
        return [
            await room.json(include_reservations=True)
            for room in await models.Room.filter(status=True)
        ]

    @staticmethod
    async def change_room_status(user, room_id, status):
        await check_admin(user)
        try:
            room = await models.Room.get(id=room_id)
        except:
            raise exceptions.RoomNotFound

        room.status = status
        await room.save()
        return {"status": "ok"}

    @staticmethod
    async def change_room_price(user, room_id, price):
        await check_admin(user)
        try:
            room = await models.Room.get(id=room_id)
        except:
            raise exceptions.RoomNotFound

        room.price = price
        await room.save()
        return {"status": "ok"}

    @staticmethod
    async def reservation_accept(user, reservation_id):
        # TODO: send email to user
        await check_admin(user)
        try:
            reservation = await models.Reservation.get(id=reservation_id)
        except:
            raise exceptions.RoomNotFound

        reservation.state = settings.ReservationState.WAIT.value

        await reservation.save()
        smtpObj = smtplib.SMTP("smtp.timeweb.ru", 25)
        msg = MIMEText(
            f"Ваша бронь одобрена!",
            "plain",
            "utf-8",
        )
        msg["Subject"] = Header("Новая бронь", "utf-8")
        msg["From"] = "support@voskresensky-hotel.ru"
        msg["To"] = reservation.email
        smtpObj.starttls()
        smtpObj.login("support@voskresensky-hotel.ru", "xxXX1234")
        smtpObj.sendmail(msg["From"], msg["To"], msg.as_string())
        smtpObj.quit()
        return {"status": "ok"}

    @staticmethod
    async def reservation_change_status(user, reservation_id, status):
        await check_admin(user)
        try:
            reservation = await models.Reservation.get(id=reservation_id)
        except:
            raise exceptions.RoomNotFound

        reservation.state = status
        await reservation.save()
        return {"status": "ok"}
