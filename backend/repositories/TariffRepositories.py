from typing import List
from models.TariffModel import Tariff
from sqlalchemy import delete, select
from schemas.TariffSchemas import TariffSchema, UpdateTariffSchema
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


"""   
{
    "2020-06-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.04"
        },
        {
            "cargo_type": "Other",
            "rate": "0.01"
        }
    ],
    "2020-07-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.035"
        },
        {
            "cargo_type": "Other",
            "rate": "0.015"
        }
    ]
}
""" 


class TariffRepositories:
    """Class for tariff repositories."""
    @staticmethod
    async def get_tariffs(session: AsyncSession) -> List[Tariff]:
        result = await session.execute(select(Tariff))
        tariffs = result.scalars().all()
        return [tariff.__dict__ for tariff in tariffs]

    @staticmethod
    async def get_tariff(tariff_id: int, session: AsyncSession) -> Tariff:
        result = await session.execute(select(Tariff).where(Tariff.id == tariff_id))
        tariff = result.scalars().first()
        return tariff.__dict__
    
    @staticmethod
    async def post_tariff(tariff: TariffSchema, session: AsyncSession) -> None:
        for date, items in tariff.data.items():
            for item in items:
                tariff_db = Tariff(
                    tariff_date=datetime.strptime(date, "%Y-%m-%d").date(),
                    cargo_type=item.cargo_type,
                    rate=item.rate
                )
                session.add(tariff_db)
        await session.commit()

    @staticmethod
    async def update_tariff(tariff_id: int, tariff: UpdateTariffSchema, session: AsyncSession) -> None:
        result = await session.execute(select(Tariff).where(Tariff.id == tariff_id))
        tariff_db = result.scalars().first()
        if tariff_db:
            if tariff.tariff_date:
                tariff_db.tariff_date = tariff.tariff_date
            if tariff.cargo_type:
                tariff_db.cargo_type = tariff.cargo_type
            if tariff.rate:
                tariff_db.rate = tariff.rate
            await session.commit()

    @staticmethod
    async def delete_tariff(tariff_id: int, session: AsyncSession) -> None:
        await session.execute(delete(Tariff).where(Tariff.id == tariff_id))
        await session.commit()
