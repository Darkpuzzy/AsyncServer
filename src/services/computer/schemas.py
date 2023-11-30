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
