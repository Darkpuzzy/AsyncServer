
from sqlalchemy import (Integer,
                        ForeignKey,
                        BigInteger, MetaData, func, TIMESTAMP, Boolean, String)
from sqlalchemy.orm import (Mapped,
                            mapped_column, DeclarativeBase)

from src.config import CONVENTION

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


class UserServerDB(BaseDBModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)