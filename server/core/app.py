from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from room.controller import room
from user.controller import user

from . import database, settings


async def lifespan(app: FastAPI):
    await database.init(
        db_url=settings.DATABASE["DB_URL"],
        modules=settings.DATABASE["MODULES"],
        generate_schemas=settings.DATABASE["GENERATE_SCHEMAS"],
    )

    yield

    await database.close()


app = FastAPI(lifespan=lifespan)
app.include_router(user, prefix="/user")
app.include_router(room, prefix="/room", tags=["room"])

app.mount("/static", StaticFiles(directory="static"), name="static")
