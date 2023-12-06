from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseComputerSchema(BaseModel):
    ram: int
    cpu: int
    disc: int
    disc_id: str


class CreateComputerSchema(BaseComputerSchema):
    connections: Optional[bool] = False


class UpdateComputerSchema(BaseComputerSchema):
    connections: Optional[bool] = False


class ResponseComputerSchema(BaseComputerSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    connections: bool


class ResponseVMSchemaWithoutDate(BaseComputerSchema):
    id: int
    connections: bool = True
