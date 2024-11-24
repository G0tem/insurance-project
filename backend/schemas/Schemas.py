from pydantic import BaseModel
from datetime import date

class Tariff(BaseModel):
    id: int
    price: int
    date: date
