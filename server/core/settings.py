import enum
import os
from typing import Literal

from dotenv import load_dotenv

# Load the stored environment variables
load_dotenv()

# -------- DataBase settings -------- #
DATABASE = {
    "DB_URL": "sqlite://database.db?charset=utf8mb4",
    "GENERATE_SCHEMAS": True,
    "MODULES": {
        "models": [
            "user.models",
            "room.models",
            "news.models",
        ],
    },
}
# -------- DataBase settings -------- #

# -------- JWT settings -------- #
ALGORITHM = "HS256"
JWT_SECRET_KEY = "secret"
TOKEN_EXPIRE = 1 * 60 * 60 * 24 * 30  # 1 month
# -------- JWT settings -------- #


# -------- Auth settings -------- #
CREATE_ADMIN_PASSWORD = "123"
# -------- Auth settings -------- #

# -------- Resrvation settings -------- #
RESRVATION_STATES_LITERAL = Literal[
    "Бронь Создана",
    "Бронь отменена",
    "Ожидаем заезд гостя",
    "Гость заехал",
    "Гость выехал",
]


class ReservationState(enum.Enum):
    CREATED = "Бронь Создана"
    CANSEL = "Бронь отменена"
    WAIT = "Ожидаем заезд гостя"
    COME = "Гость заехал"
    LEFT = "Гость выехал"


PARKING_PLACES = 15

# -------- Resrvation settings -------- #
