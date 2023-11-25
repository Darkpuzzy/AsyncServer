from passlib.hash import bcrypt
from sqlalchemy import select

from src.core.bases.utils.logger.conf import LOGGER
from src.services.users.models import UserServerDB
from src.core.bases.base_dao import BaseDAO
from src.db.database import async_session_maker


class UserDAO(BaseDAO):
    model = UserServerDB
    session = async_session_maker

    @classmethod
    async def get_by_username(
            cls,
            username: str
    ) -> dict:
        try:
            async with cls.session() as ses:
                query = select(
                    cls.model
                ).where(
                    cls.model.username == username)
                response = await ses.execute(query)
                print(response)
                result = await cls._as_dict(response)
                print(result)
                if not result:
                    raise Exception("User not found")
                return result
        except Exception as err:
            LOGGER.exception("BaseDAO ERROR")
            raise Exception(f"{cls.model.__name__} {err}")


class UserManager:

    @classmethod
    async def registered(cls, password: str, username: str):
        hashed_password = bcrypt.hash(password)
        return await UserDAO.create(data={"username": username,
                                          "password": hashed_password})

    @classmethod
    async def login(cls, password: str, username: str):
        try:
            user_model_data: dict = await UserDAO.get_by_username(username=username)
            if user_model_data:
                if bcrypt.verify(password, user_model_data.get("password")):
                    LOGGER.info("SUCCESS PASSWORD")
                    return 1
                else:
                    LOGGER.info("WRONG PASSWORD")
                    return 0
            LOGGER.info("USER NOT FOUND")
            return 0
        except Exception as err:
            LOGGER.exception(err)
