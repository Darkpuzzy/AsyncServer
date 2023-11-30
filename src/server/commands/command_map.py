import json
from typing import Annotated

from passlib.hash import bcrypt

from src.core.bases.base_exceptions import UnknownBaseError
from src.core.bases.utils.custom_dec.auth_dec import check_user_auth
from src.core.bases.utils.logger.conf import LOGGER
from src.server.commands.commander import ServerCommander
from src.services.users.subservices import UserManager

COMMANDS_MAPS = {
    "ping": Annotated[ServerCommander.ping, "pong answer"],
    "help": ServerCommander.help,
    "connect": ServerCommander.connection
}


async def commander(msg: str):
    try:
        answer = COMMANDS_MAPS.get(msg)
        if answer:
            return await COMMANDS_MAPS.get(msg)()
        raise UnknownBaseError(msg)
    except Exception as err:
        return f" --- Traceback --- \n {err}"


async def loggin(user_data: str) -> str:
    try:
        data: dict = json.loads(user_data)
        username = data.get("username")
        password = data.get("password")

        hashed_password: str = bcrypt.hash(password)
        if await UserManager.login(username=username, password=password):
            return await ServerCommander.add_user_secret_token(
                username=username,
                password=hashed_password
            )
        return "Failed auth"
    except Exception as err:
        LOGGER.exception(err)


async def token_check(token: str):
    with open("server_creds.json", "r") as f:
        fr = f.read()
        if fr:
            data = json.loads(fr)
            data.get(token)
            if data:
                return 1
        else:
            return 0


async def register(user_data: str) -> bool:
    try:
        data: dict = json.loads(user_data)
        username_r = data.get("username")
        password_r = data.get("password")
        await UserManager.registered(username=username_r, password=password_r)
        return 1
    except Exception as err:
        LOGGER.exception(err)
