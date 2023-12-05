
from ...db.database import async_session_maker
from .models import VirtualComputer
from ...core.bases.base_dao import BaseDAO


class ComputerDAO(BaseDAO):
    model = VirtualComputer
    session = async_session_maker


