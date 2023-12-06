from typing import List, AsyncGenerator

from .schemas import (
    ResponseComputerSchema,
    CreateComputerSchema,
    UpdateComputerSchema,
    ResponseVMSchemaWithoutDate)
from .subservices import ComputerDAO


async def get_all_generator() -> AsyncGenerator:
    for item in await ComputerDAO.get_all():
        yield ResponseVMSchemaWithoutDate(**item).model_dump()


async def get_all() -> List[ResponseComputerSchema]:
    return await ComputerDAO.get_all()


async def get_by_id(comp_id: int) -> ResponseVMSchemaWithoutDate:
    return ResponseVMSchemaWithoutDate(**await ComputerDAO.get_by_id(obj_id=comp_id))


async def create(data: CreateComputerSchema) -> ResponseVMSchemaWithoutDate:
    return ResponseVMSchemaWithoutDate(**await ComputerDAO.create(data=data.__dict__))


async def total_ram() -> int:
    result: int = await ComputerDAO.get_all_ram()
    return result


async def total_cpu() -> int:
    result: int = await ComputerDAO.get_all_cpu()
    return result


async def total_disc() -> int:
    result: int = await ComputerDAO.get_all_disk()
    return result


async def get_total_info() -> dict:
    result = {
        "total_vm"  : len(await get_all()),
        "total_ram" : await total_ram(),
        "total_cpu" : await total_cpu(),
        "total_disc": await total_disc()
    }
    return result


async def update(
        comp_id: id,
        data: UpdateComputerSchema
) -> ResponseComputerSchema:
    return await ComputerDAO.update(obj_id=comp_id, data=data.__dict__)


async def delete(
        comp_id: int
) -> dict:
    return await ComputerDAO.delete(obj_id=comp_id)
