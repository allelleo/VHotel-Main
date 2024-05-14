import datetime

from core import settings
from fastapi import APIRouter, Request, Depends
from user import depends
from actions.models import Action

actions = APIRouter()


@actions.post("/create")
async def create_action(r: Request, content: str, usr=Depends(depends.get_user)):
    action = await Action.create(content=content)
    return await action.json()


@actions.get("/")
async def get_actions(r: Request):
    data = []
    for act in await Action.all():
        data.append(await act.json())
    return data


@actions.get("/{id}")
async def get_news_by_id(r: Request, id: int):
    act = await Action.get(id=id)
    return await act.json()


@actions.delete("/{id}")
async def delete_action(r: Request, id: int):
    act = await Action.get(id=id)
    await act.delete()
    return {"status": "ok"}
