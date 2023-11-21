from src.core.bases.base_database import BaseDBModel

from enum import Enum

from sqlalchemy.dialects import ENUM as PgEnum
from sqlalchemy import (Integer,
                        ForeignKey,
                        BigInteger)
from sqlalchemy.orm import (Mapped,
                            mapped_column)


class VirtualComputer(BaseDBModel):
    __tablename__ = "virtual_computer"
    """
    Уникальный идентификатор (ID).
    Объем выделенной RAM.
    Количество выделенных CPU.
    Объем памяти жесткого диска.
    Уникальнный индентификатор жесткого диска(ID)
    """
    v_ram: Mapped[int] = mapped_column(Integer, nullable=False)
    v_cpu: Mapped[int] = mapped_column(Integer, nullable=False)
    v_disk: Mapped[int] = mapped_column(Integer, nullable=False)
    disc_id: Mapped[int] = mapped_column(
        BigInteger, autoincrement=True, nullable=False, unique=True, primary_key=True, index=True
    )
