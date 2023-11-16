
from typing import Dict, List, Self

from sqlalchemy import ChunkedIteratorResult, insert, or_, select, update
from sqlalchemy.orm.attributes import instance_dict

from src.core.bases.base_exceptions import DataBaseOperationError
from utils.logger.conf import LOGGER


class BaseDAO:
    session = None
    model = None

    @classmethod
    async def get_all(cls):
        try:
            async with cls.session() as ses:
                query = select(
                    cls.model
                ).where(
                    cls.model.archived.is_(False))
                response = await ses.execute(query)
                res = await cls._as_dict(response=response,
                                         type_response=list)
                return res
        except Exception:
            LOGGER.exception("BaseDAO ERROR")
            raise DataBaseOperationError(f"{cls.model.__name__} ERROR")

    @classmethod
    async def get_by_id(  # TODO IF RES IS NOT -> ....
            cls,
            obj_id: int
    ):
        try:
            async with cls.session() as ses:
                query = select(
                    cls.model
                ).where(
                    cls.model.id == obj_id,
                    cls.model.archived.is_(False))
                response = await ses.execute(query)
                result = await cls._as_dict(response=response)
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
            data: dict,
            user_id: int
    ):  # FIXME: returned all model fields
        try:
            data = {key: val for key, val in data.items() if val is not None}
            async with cls.session() as ses:
                stmt = update(
                    cls.model
                ).where(
                    cls.model.id == obj_id,
                    cls.model.user_id == user_id,
                    cls.model.archived.is_(False)
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
            obj_id: int,
            user_id: int
    ):
        try:
            async with cls.session() as ses:
                stmt = update(
                    cls.model
                ).where(
                    cls.model.id == obj_id,
                    cls.model.user_id == user_id,
                    cls.model.archived.is_(False)
                ).values(
                    archived=True
                ).returning(
                    cls.model
                )
                res = await ses.execute(stmt)
                await ses.commit()
                res = res.fetchone()
                if not res or res is None:
                    raise DataBaseOperationError("Not yours or already deleted ")
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
    def from_dict(cls, data: dict) -> Self:
        valid_data: dict = {key: value for key, value in data.items() if key in cls.__dict__}
        return cls(**valid_data)

    @classmethod
    def to_dict(cls) -> dict:
        result: dict = {key: value for key, value in cls.__dict__.items() if not key.startswith('_')}
        return result

