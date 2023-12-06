import json
from typing import AsyncGenerator

from src.services.computer import create, get_all_generator, get_by_id

from src.services.computer.schemas import CreateComputerSchema
from src.services.computer.actions import (
    get_all,
    total_ram,
    total_cpu,
    total_disc,
    get_total_info,
    delete)


class ServerCommander:

    admins_commands: str = """

    'active-connections' -> Show active connections VM
    update_con -> Updated statuses VM in active connections\n

    ### INFO ###\n

    'all_ram' -> Show total ram
    'all_cpu' -> total cpu
    'all_cd_size' -> total disc size
    'all_info' -> Show total info from DB for VM

    ### INFO VM ###
    show_all -> all VM from DB
    show_obj {id} -> full info for VM from DB
    delete_obj {id} -> delete VM from DB
    """

    server_command: str = """
    ### SERVER COMMANDS ###
    ping -> pong
    connect -> init connection to the server for VM! Connect in active connections
    help -> help list
    show_me -> if your VM connected you see cpu, ram and another...
    """

    @classmethod
    async def permissions_attention(cls) -> str:
        return "You don have permission"

    @classmethod
    async def ping(cls) -> str:
        return "pong"

    @classmethod
    async def help(
            cls
    ) -> str:
        return cls.server_command

    @classmethod
    async def help_admin(
            cls
    ) -> str:
        return cls.admins_commands + cls.server_command

    @classmethod
    async def connection(
            cls,
            data: dict
    ):
        response = await create(data=CreateComputerSchema(**data))
        return response

    @classmethod
    async def show_all_from_db(
            cls,
            admin: bool = None
    ) -> AsyncGenerator:
        return get_all_generator

    @classmethod
    async def show_by_id(
            cls,
            obj_id: int
    ) -> dict:
        response = await get_by_id(comp_id=obj_id)
        return response.model_dump()

    @classmethod
    async def delete_obj(
            cls,
            obj_id: int
    ) -> dict:
        response: dict = await delete(comp_id=obj_id)
        return response

    @classmethod
    async def update_obj(
            cls,
            obj_id: int,
            data
    ):
        ...

    @classmethod
    async def get_total_cpu(cls) -> str:
        result: int = await total_cpu()
        return f"TOTAL CPU: {result} core"

    @classmethod
    async def get_total_ram(cls) -> str:
        result: int = await total_ram()
        return f"TOTAL RAM: {result} GB"

    @classmethod
    async def get_total_disc(cls) -> str:
        result: int = await total_disc()
        return f"TOTAL DISC: {result} GB"

    @classmethod
    async def all_usage_stats(
            cls
    ) -> str:
        result: dict = await get_total_info()
        return json.dumps(result)

    @classmethod
    async def count_vm(
            cls
    ) -> int:
        result: list = await get_all()
        return len(result)

