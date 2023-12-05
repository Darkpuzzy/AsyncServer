import asyncio
from typing import List, AsyncGenerator

from .schemas import ResponseComputerSchema, CreateComputerSchema, UpdateComputerSchema, \
    ResponseVMSchemaWithoutDate
from .subservices import ComputerDAO


async def get_all() -> AsyncGenerator:
    for item in await ComputerDAO.get_all():
        yield ResponseVMSchemaWithoutDate(**item).model_dump()


async def get_by_id(comp_id: int) -> ResponseVMSchemaWithoutDate:
    return ResponseVMSchemaWithoutDate(**await ComputerDAO.get_by_id(obj_id=comp_id))


async def create(data: CreateComputerSchema) -> ResponseVMSchemaWithoutDate:
    return ResponseVMSchemaWithoutDate(**await ComputerDAO.create(data=data.__dict__))


async def update(
        comp_id: id,
        data: UpdateComputerSchema
) -> ResponseComputerSchema:
    return await ComputerDAO.update(obj_id=comp_id, data=data.__dict__)


# async def tests():
#     print("TEST")
#     print(type(get_all))
#     async for obj in get_all():
#         print(obj)
#
# print(asyncio.run(tests()))