
from sqlalchemy import MetaData, BigInteger, func, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import CONVENTION


class BaseDB(DeclarativeBase):
    metadata = MetaData(naming_convention=CONVENTION)


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



