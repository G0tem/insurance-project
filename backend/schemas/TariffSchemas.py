from pydantic import BaseModel
from datetime import date

class Tariff(BaseModel):
    id: int
    price: int
    tariff_date: date

class TariffCreate(BaseModel):
    price: int
    tariff_date: date