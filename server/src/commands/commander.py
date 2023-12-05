from ..services.computer import create
from src.services.computer.schemas import CreateComputerSchema


class ServerCommander:

    admins_commands: str = """
    'active-connections' -> Show active connections VM\n
    ### INFO ###\n
    'all_ram' -> Show all active ram\n
    'all_cpu' ->\n
    'all_cd_size' ->\n
    'all_disc_id' -> \n
    
    ### INFO BY ID ###\n
    get-vm-{id} -> full info for VM\n
    
    ### SET ATTRIBUTE ###\n
    set-vm-{id} cpu/ram/disk_size {arg: int} \n
    """

    server_command: str = """
    ### SERVER COMMANDS ###\n
    ping -> pong\n
    connect -> init connection to the server for VM!\n
    help -> help list
    """

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
