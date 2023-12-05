from typing import AsyncGenerator

from src.services.computer import create, get_all, get_by_id
from src.services.computer.schemas import CreateComputerSchema


class ServerCommander:

    admins_commands: str = """
    
    'active-connections' -> Show active connections VM\n
    update_con -> Updated statuses VM in active connections\n
    
    ### INFO ###\n
    
    'all_ram' -> Show all active ram\n
    'all_cpu' ->\n
    'all_cd_size' ->\n
    'all_disc_id' -> \n
    
    ### INFO VM ###\n
    show_all -> all VM from DB\n
    show_obj {id} -> full info for VM from DB\n  
    delete_obj {id} -> delete VM from DB\n
    """

    server_command: str = """
    ### SERVER COMMANDS ###\n
    ping -> pong\n
    connect -> init connection to the server for VM! Connect in active connections\n
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
            cls,
            admin_status: bool = False
    ) -> str:
        if admin_status:
            return cls.admins_commands + cls.server_command
        return cls.server_command

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
        return get_all

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
    ):
        ...

    @classmethod
    async def update_obj(
            cls,
            obj_id: int,
            data
    ):
        ...
