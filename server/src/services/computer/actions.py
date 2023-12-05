from typing import List

from .schemas import ResponseComputerSchema, CreateComputerSchema, UpdateComputerSchema, \
    ResponseVMSchemaWithoutDate
from .subservices import ComputerDAO


async def get_all() -> List[ResponseComputerSchema]:
    return await ComputerDAO.get_all()


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
#     # print(await get_all())
#     print(ResponseComputerSchema(**await get_by_id(12)).__dict__)
#
#
#
# print(asyncio.run(tests()))