from typing import Annotated

from .commander import ServerCommander
from src.core.bases.base_exceptions import UnknownBaseError

COMMANDS_MAPS = {
    "ping": Annotated[ServerCommander.ping, "pong answer"],
    "help": {False: ServerCommander.help,
             True: ServerCommander.help},
    "connect": "success connect",
}


async def commander_maps(
        msg: str,
        data: bool = False,
        admin: bool = False
):
    try:
        answer = COMMANDS_MAPS.get(msg)
        if answer:
            if admin:
                if isinstance(answer, dict):
                    answer = await COMMANDS_MAPS.get(msg).get(admin)(True)
                    print("ANSWER", answer)
                    return answer
                return await COMMANDS_MAPS.get(msg)()
            if isinstance(answer, dict):
                return await COMMANDS_MAPS.get(msg).get(False)()
            return await COMMANDS_MAPS.get(msg)()
        raise UnknownBaseError(msg)
    except Exception as err:
        print(err)
        return f" --- Traceback --- \n {err}"