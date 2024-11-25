from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Date
from database import Base


class Tariff(Base):
    __tablename__ = "tariff"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float]
    tariff_date: Mapped[Date] = mapped_column(Date())