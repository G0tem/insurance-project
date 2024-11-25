from pydantic import BaseModel
from datetime import date

class Tariff(BaseModel):
    id: int
    price: float
    tariff_date: date

class TariffCreate(BaseModel):
    price: float
    tariff_date: date