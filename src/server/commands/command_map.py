from src.core.bases.base_exceptions import UnknownBaseError

COMMANDS_MAPS = {
    "ping": "pong",
    "server.help": " | ping ---> pong\n | help ---> commands list"
}


async def commander(msg: str):
    try:
        answer = COMMANDS_MAPS.get(msg)
        if answer:
            return COMMANDS_MAPS.get(msg)
        raise UnknownBaseError(msg)
    except Exception as err:
        return f" --- Traceback --- \n {err}"