from typing import List
from kafka_log.Message import Message
from models.TariffModel import Tariff
from sqlalchemy import delete, select
from schemas.TariffSchemas import TariffSchema, UpdateTariffSchema
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


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
        count = 0
        for date, items in tariff.data.items():
            for item in items:
                tariff_db = Tariff(
                    tariff_date=datetime.strptime(date, "%Y-%m-%d").date(),
                    cargo_type=item.cargo_type,
                    rate=item.rate
                )
                session.add(tariff_db)
                count += 1
        await session.commit()
        await Message.log_action('post_tariff, tariffs added: ' + str(count))

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
            await Message.log_action('update_tariff with id: ' + str(tariff_id))

    @staticmethod
    async def delete_tariff(tariff_id: int, session: AsyncSession) -> None:
        await session.execute(delete(Tariff).where(Tariff.id == tariff_id))
        await session.commit()
        await Message.log_action('delete_tariff with id: ' + str(tariff_id))
