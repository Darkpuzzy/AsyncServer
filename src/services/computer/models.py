
from sqlalchemy import (Integer,
                        ForeignKey,
                        BigInteger, MetaData, func, TIMESTAMP, Boolean)
from sqlalchemy.orm import (Mapped,
                            mapped_column, DeclarativeBase)

from config import CONVENTION

metadata = MetaData(naming_convention=CONVENTION)


class BaseDB(DeclarativeBase):
    metadata = metadata


class BaseDBModel(BaseDB):

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        BigInteger, autoincrement=True, nullable=False, unique=True, primary_key=True, index=True
    )
    created_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=func.current_timestamp(),
        comment='Created datetime'
    )
    updated_at: Mapped[int] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
        comment='Last update datetime'
    )


class VirtualComputer(BaseDBModel):

    __tablename__ = "virtual_computer"

    v_ram: Mapped[int] = mapped_column(Integer, nullable=False)
    v_cpu: Mapped[int] = mapped_column(Integer, nullable=False)
    v_disk: Mapped[int] = mapped_column(Integer, nullable=False)
    disc_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True, index=True
    )
    connections: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)