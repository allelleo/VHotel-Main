import datetime

from pydantic import BaseModel, EmailStr


class ReservationRequest(BaseModel):
    date_in: datetime.date
    date_out: datetime.date
    car_place: int
    guest_count: int
    phone: str
    first_name: str
    last_name: str
    room_type: str
    email: EmailStr
