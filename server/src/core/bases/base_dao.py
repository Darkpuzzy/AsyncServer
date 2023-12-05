
from typing import Dict, List

from sqlalchemy import ChunkedIteratorResult, insert, select, update, delete
from sqlalchemy.orm.attributes import instance_dict

from .base_exceptions import DataBaseOperationError
from .utils.logger.conf import LOGGER


class BaseDAO:
    session = None
    model = None

    @classmethod
    async def get_all(cls):
        try:
            async with cls.session() as ses:
                query = select(
                    cls.model
                )
                response = await ses.execute(query)
                res = await cls._as_dict(response=response,
                                         type_response=list)
                return res
        except Exception:
            LOGGER.exception("BaseDAO ERROR")
            raise DataBaseOperationError(f"{cls.model.__name__} ERROR")

    @classmethod
    async def get_by_id(
            cls,
            obj_id: int
    ):
        try:
            async with cls.session() as ses:
                query = select(
                    cls.model
                ).where(
                    cls.model.id == obj_id)
                response = await ses.execute(query)
                obj = response.scalar_one_or_none()
                result = await cls.to_dict(obj)
                if not result:
                    raise DataBaseOperationError("Object not found")
                return result
        except DataBaseOperationError as err:
            LOGGER.exception("BaseDAO ERROR")
            raise DataBaseOperationError(f"{cls.model.__name__} {err}")

    @classmethod
    async def create(
            cls,
            data: dict
    ):
        try:
            async with cls.session() as ses:
                stmt = insert(
                    cls.model
                ).values(
                    **data
                ).returning(
                    cls.model
                )
                result = await ses.execute(stmt)
                await ses.commit()
                row = await cls._as_dict(response=result)
                return row
        except Exception:
            LOGGER.exception("BaseDAO ERROR")
            raise DataBaseOperationError(f"{cls.model.__name__} ERROR")

    @classmethod
    async def update(
            cls,
            obj_id: int,
            data: dict
    ):  # FIXME: returned all model fields
        try:
            data = {key: val for key, val in data.items() if val is not None}
            async with cls.session() as ses:
                stmt = update(
                    cls.model
                ).where(
                    cls.model.id == obj_id,
                ).values(
                    **data
                ).returning(
                    cls.model
                )
                result = await ses.execute(stmt)
                await ses.commit()
                row = await cls._as_dict(response=result)
                if not row:
                    raise DataBaseOperationError("Nothing Update")
                return row
        except Exception:
            LOGGER.exception("----> BaseDAO ERROR")
            raise DataBaseOperationError(f"{cls.model.__name__} ERROR")

    @classmethod
    async def delete(
            cls,
            obj_id: int
    ):
        try:
            async with cls.session() as ses:
                stmt = delete(
                    cls.model
                ).where(
                    cls.model.id == obj_id
                )
                res = await ses.execute(stmt)
                await ses.commit()
                return {"DELETED"}
        except Exception as err:
            LOGGER.exception("BaseDAO ERROR")
            raise DataBaseOperationError(f"{cls.model.__name__} ERROR {err}")

    @classmethod
    async def _as_dict(
            cls,
            response: ChunkedIteratorResult,
            type_response: type = None
    ) -> Dict | List:
        result = response.scalars().all()
        try:
            if type_response is None and result:
                return instance_dict(result[0])
            elif type_response is list and result:
                return [instance_dict(obj) for obj in result]
            return result
        except Exception as err:
            LOGGER.exception(f"BaseDAO as_dict ERROR: {err}")
            raise DataBaseOperationError(f"{cls.model.__name__} ERROR")

    @classmethod
    async def to_dict(cls, obj) -> dict:
        result: dict = {key: value for key, value in obj.__dict__.items() if not key.startswith('_')}
        return result

