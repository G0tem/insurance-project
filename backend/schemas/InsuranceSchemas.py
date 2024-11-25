from decimal import Decimal
from pydantic import BaseModel


class InsuranceSchema(BaseModel):
    insurance_date: str
    cargo_type: str
    declared_cost: Decimal
    