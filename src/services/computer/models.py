from src.core.bases.base_database import BaseDBModel

from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy import (Integer,
                        String,
                        Boolean,
                        ForeignKey,
                        DateTime,
                        BigInteger,
                        func)
from sqlalchemy.dialects.postgresql import (TIMESTAMP,
                                            JSONB,
                                            JSON)
from sqlalchemy.orm import (Mapped,
                            mapped_column)


class VirtualComputer(BaseDBModel):
    ...
