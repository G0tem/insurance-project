from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.types import Date


Base = declarative_base()

class Tariff(Base):
    __tablename__ = "tariff"

    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[int]
    tariff_date: Mapped[Date] = mapped_column(Date())