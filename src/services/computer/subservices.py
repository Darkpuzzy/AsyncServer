from src.core.bases.base_dao import BaseDAO
from src.db.database import async_session_maker
from .models import VirtualComputer


class ComputerDAO(BaseDAO):
    model = VirtualComputer
    session = async_session_maker


