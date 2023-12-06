from typing import Annotated

from .commander import ServerCommander
from src.core.bases.base_exceptions import UnknownBaseError

COMMANDS_MAPS = {
    "ping"      : Annotated[ServerCommander.ping, "pong answer"],
    "help"      : {False: ServerCommander.help,
                    True: ServerCommander.help_admin},
    "connect"   : "success connect",
    "show_all"  : {True: ServerCommander.show_all_from_db,
                    False: ServerCommander.permissions_attention},
    "show_obj"  : ServerCommander.show_by_id,
    "all_ram"   :  {True: ServerCommander.get_total_ram,
                    False: ServerCommander.permissions_attention},
    "all_cpu"   : {True: ServerCommander.get_total_cpu,
                    False: ServerCommander.permissions_attention},
    "all_disc"  : {True: ServerCommander.get_total_disc,
                    False: ServerCommander.permissions_attention},
    "all_info"  : {True: ServerCommander.all_usage_stats,
                    False: ServerCommander.permissions_attention},
    "all_vm"    : {True: ServerCommander.count_vm,
                    False: ServerCommander.permissions_attention},
    "delete_obj": ServerCommander.delete_obj,

}


async def commander_maps(
        msg: str,
        data: bool = False,
        admin: bool = False
):
    try:

        if "show_obj" in msg:
            obj_id = int(msg.replace("show_obj ", "").replace(" ", ""))
            if isinstance(obj_id, int):
                return await COMMANDS_MAPS.get("show_obj")(obj_id=obj_id)
            raise UnknownBaseError("ID must be int not str")
        if "delete_obj" in msg:
            if admin:
                obj_id = int(msg.replace("delete_obj ", "").replace(" ", ""))
                if isinstance(obj_id, int):
                    return await COMMANDS_MAPS.get("delete_obj")(obj_id=obj_id)
                raise UnknownBaseError("ID must be int not str")
            return await COMMANDS_MAPS.get("show_all").get(False)()

        answer = COMMANDS_MAPS.get(msg)

        if answer:
            if admin:
                if isinstance(answer, dict):
                    answer = await COMMANDS_MAPS.get(msg).get(admin)()
                    print("ANSWER", answer)
                    return answer
                return await COMMANDS_MAPS.get(msg)()
            if isinstance(answer, dict):
                return await COMMANDS_MAPS.get(msg).get(False)()
            return await COMMANDS_MAPS.get(msg)()
        raise UnknownBaseError(msg)
    except Exception as err:
        print(err)
        print("TRACEBACK")
        return f" --- Traceback --- \n {err}"
