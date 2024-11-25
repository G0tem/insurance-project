from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Date
from database import Base
from decimal import Decimal


class Insurance(Base):
    __tablename__ = "insurance"

    id: Mapped[int] = mapped_column(primary_key=True)
    insurance_date: Mapped[Date] = mapped_column(Date())
    cargo_type: Mapped[str]
    declared_cost: Mapped[Decimal] = mapped_column(Numeric(asdecimal=True, scale=2))
    insurance_cost: Mapped[Decimal] = mapped_column(Numeric(asdecimal=True, scale=2))
