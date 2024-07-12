import datetime
from fastapi import File, UploadFile
from core import settings
from fastapi import APIRouter, Request, Depends
from user import depends
from news.models import News
import random

news = APIRouter()


@news.post("/create")
async def create_news(
    r: Request,
    title: str,
    link: str,
    file: UploadFile = File(...),
    usr=Depends(depends.get_user),
):
    contents = file.file.read()
    filename = f"static/{random.randint(0, 100)}_{file.filename}"
    with open(f"{filename}", "wb") as f:
        f.write(contents)
    news = await News.create(title=title, link=link, image=filename)
    return await news.json()


@news.get("/")
async def get_news(r: Request):
    data = []
    for news in await News.all():
        data.append(await news.json())
    return data


@news.get("/{id}")
async def get_news_by_id(r: Request, id: int):
    news = await News.get(id=id)
    return await news.json()


@news.delete("/{id}")
async def delete_news(r: Request, id: int):
    news = await News.get(id=id)
    await news.delete()
    return {"status": "ok"}
