from schemas.InsuranceSchemas import InsuranceSchema
from sqlalchemy.ext.asyncio import AsyncSession
from models.InsuranceModel import Insurance
from models.TariffModel import Tariff
from sqlalchemy import select
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy import insert
from datetime import date


class InsuranceRepositories:
    """Class for insurance repositories."""

    @staticmethod
    async def post_insurance(insurance: InsuranceSchema, session: AsyncSession) -> None:
        rate = await InsuranceRepositories.get_rate(insurance, session)
        total_cost = insurance.declared_cost * Decimal(str(rate))
        total_cost = total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        await InsuranceRepositories.save_insurance_result(insurance, total_cost, session)
        return {"стоимость страхования": total_cost}

    @staticmethod    
    async def get_rate(insurance: InsuranceSchema, session: AsyncSession) -> float:
        insurance_date = datetime.strptime(insurance.insurance_date, "%Y-%m-%d").date()
        query = select(Tariff).where(
            Tariff.tariff_date == insurance_date,
            Tariff.cargo_type == insurance.cargo_type
        )
        result = await session.execute(query)
        tariff_model = result.scalars().first()

        if tariff_model:
            return tariff_model.rate
        else:
            raise Exception("Tariff not found for the provided insurance details")

    @staticmethod
    async def save_insurance_result(insurance: InsuranceSchema, total_cost: Decimal, session: AsyncSession) -> None:
        insurance_date = date.fromisoformat(insurance.insurance_date)

        insurance_data = {
            "insurance_date": insurance_date,
            "cargo_type": insurance.cargo_type,
            "declared_cost": insurance.declared_cost,
            "insurance_cost": total_cost
        }

        stmt = insert(Insurance).values(insurance_data)

        await session.execute(stmt)
        await session.commit()
