import asyncio
from typing import List

from .schemas import ResponseComputerSchema, CreateComputerSchema, UpdateComputerSchema
from .subservices import ComputerDAO


async def get_all() -> List[ResponseComputerSchema]:
    return await ComputerDAO.get_all()


async def get_by_id(comp_id: int) -> ResponseComputerSchema:
    return await ComputerDAO.get_by_id(obj_id=comp_id)


async def create(data: CreateComputerSchema) -> ResponseComputerSchema:
    return await ComputerDAO.create(data=data.__dict__)


async def update(
        comp_id: id,
        data: UpdateComputerSchema
) -> ResponseComputerSchema:
    return await ComputerDAO.update(obj_id=comp_id, data=data.__dict__)