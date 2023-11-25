from datetime import date
from typing import Optional

from pydantic import BaseModel


class BaseComputerSchema(BaseModel):
    v_ram: int
    v_cpu: int
    v_disk: int
    disc_id: int


class CreateComputerSchema(BaseComputerSchema):
    connections: Optional[bool] = False


class UpdateComputerSchema(BaseComputerSchema):
    connections: Optional[bool] = False


class ResponseComputerSchema(BaseComputerSchema):
    id: int
    created_at: date
    updated_at: date
    connections: bool


class VirtualMachine:
    def __init__(
            self,
            id,
            ram,
            cpu,
            disk_size,
            disk_id
    ):
        self.id = id
        self.ram = ram
        self.cpu = cpu
        self.disk_size = disk_size
        self.disk_id = disk_id
