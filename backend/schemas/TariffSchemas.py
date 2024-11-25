from pydantic import BaseModel
from typing import List
from datetime import date


class Tariff(BaseModel):
    cargo_type: str
    rate: float

class Tariffs(BaseModel):
    date: date
    rates: List[Tariff]
