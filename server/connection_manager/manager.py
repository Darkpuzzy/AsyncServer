import asyncio
import json


class ConnectManager:

    admin_connections = {}
    active_connections = {}

    @classmethod
    async def add_to_adm_con(
            cls,
            writer: asyncio.StreamWriter,
            addr: tuple
    ) -> None:
        cls.admin_connections[writer] = {
            "status": True,
            "info": None,
            "addr": addr
        }

    @classmethod
    async def add_to_default_con(
            cls,
            writer: asyncio.StreamWriter,
            addr: tuple
    ) -> None:
        cls.active_connections[writer] = {
            "status": True,
            "info": None,
            "addr": addr
        }

    @classmethod
    async def show_me(
            cls,
            writer: asyncio.StreamWriter
    ) -> str:
        try:
            data = cls.active_connections.get(writer).get("info")
            if data:
                response: str = await cls._to_json(obj=data.__dict__)
                return response
            return "not data, please connect"
        except Exception as err:
            print(err)

    @classmethod
    async def update_info_by_writer(
            cls,
            writer: asyncio.StreamWriter,
            data
    ) -> str:
        cls.active_connections[writer]["info"] = data
        cls.active_connections[writer]["status"] = True
        return "Updated"

    @classmethod
    async def update_statuses(
            cls,
            reader: asyncio.StreamReader,
            writer: asyncio.StreamWriter,
            answer: str = None
    ) -> str:
        if answer == "admin_pong":
            cls.active_connections.get(writer)["status"] = True
        else:
            cls.active_connections.get(writer)["status"] = False
        print(cls.active_connections)
        return f"Updated active_connections - {len(cls.active_connections)}"

    @classmethod
    async def _to_json(
            cls,
            obj: dict
    ) -> str:
        result: str = json.dumps(obj)
        return result

    @classmethod
    async def show_all_connections(
            cls
    ) -> str:
        try:
            print("ADMINS", cls.admin_connections)

            response_data = f"Admins-------------------:\n{cls.admin_connections}\nVM-------------------:\n{cls.active_connections}"
            return response_data
        except Exception as err:
            print("SERVER ERROR", err)
