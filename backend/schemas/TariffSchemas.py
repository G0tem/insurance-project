from datetime import date
from typing import Optional
from pydantic import BaseModel


class TariffItem(BaseModel):
    cargo_type: str
    rate: float

class TariffSchema(BaseModel):
    data: dict[str, list[TariffItem]]

class UpdateTariffSchema(BaseModel):
    tariff_date: Optional[date]
    cargo_type: Optional[str]
    rate: Optional[float]
