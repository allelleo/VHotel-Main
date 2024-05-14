from fastapi import HTTPException
from starlette import status


class RoomNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Room not found."}
        )


class UserNotAdmin(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN, detail={"message": "User not admin."}
        )


class RoomTypeNotFound(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Room by type not found."},
        )


class ParkingPlaces(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "Car places not found."},
        )


class ReservationFail(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "Reservation Fail."},
        )


class DatesFail(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "Dates Fail."},
        )
