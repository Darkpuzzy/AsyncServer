
from src.db.database import async_session_maker
from .models import VirtualComputer
from src.core.bases.base_dao import BaseDAO

from sqlalchemy import text


class ComputerDAO(BaseDAO):
    """
    This class have base crud:

    @get_all
    @get_by_id
    @create
    @update
    @delete

    and have specials methods:

    @get_all_ram -> int - returned sum Model.ram
    @get_all_cpu -> int - returned sum Model.cpu
    @get_all_disk -> int - returned sum Model.disk

    """

    model = VirtualComputer
    session = async_session_maker

    @classmethod
    async def get_all_ram(cls):
        table_name = cls.model.__table__
        async with cls.session() as ses:
            stmt = text(
                f"""
                SELECT SUM({table_name}.ram)
                FROM {table_name}
                """
            )
            response = await ses.execute(stmt)
            result = response.scalar()
            return result

    @classmethod
    async def get_all_cpu(cls):
        table_name = cls.model.__table__
        async with cls.session() as ses:
            stmt = text(
                f"""
                SELECT SUM({table_name}.cpu)
                FROM {table_name}
                """
            )
            response = await ses.execute(stmt)
            result = response.scalar()
            return result

    @classmethod
    async def get_all_disk(cls):
        table_name = cls.model.__table__
        async with cls.session() as ses:
            stmt = text(
                f"""
                SELECT SUM({table_name}.disc)
                FROM {table_name}
                """
            )
            response = await ses.execute(stmt)
            result = response.scalar()
            return result

