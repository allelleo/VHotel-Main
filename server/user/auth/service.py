from core import settings
from tortoise.transactions import in_transaction
from user import models, token
from user.auth import exceptions, schemas


async def sign_up(data: schemas.SignUpRequest):
    if not data.create_admin_password == settings.CREATE_ADMIN_PASSWORD:
        raise exceptions.WrongAdminCreatePasswordException
    if await models.User.exists(email=data.email):
        raise exceptions.EmailExistsException
    if await models.User.exists(username=data.username):
        raise exceptions.UsernameExistsException

    async with in_transaction() as transaction:
        user = models.User(
            email=data.email,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            is_admin=True,
        )
        await user.set_password(data.password)
        await user.save(using_db=transaction)

    return {"satus": "ok", "user_id": user.id}


async def sign_in(data: schemas.SignInRequest):
    if not await models.User.exists(email=data.email):
        raise exceptions.UserNotFoundByEmailException

    user = await models.User.get(email=data.email)

    if await user.check_password(data.password):
        if user.is_admin:
            return {"token": await token.create_token({"user_id": user.id})}
        raise exceptions.WrongAdminCreatePasswordException
    raise exceptions.WrongPasswordException
