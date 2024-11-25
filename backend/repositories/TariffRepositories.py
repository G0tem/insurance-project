from fastapi import HTTPException
from models.TariffModel import Tariff
from sqlalchemy import select
from schemas.TariffSchemas import TariffCreate


class TariffRepositories:
    """Class for tariff repositories."""

    async def get_tariff(session):
        tariffs = await session.execute(
            select(Tariff).order_by(Tariff.id)
        )
        return [
            {
                "id": tariff.id,
                "price": tariff.price,
                "tariff_date": tariff.tariff_date,
            }
            for tariff in tariffs.scalars().all()
        ]

    async def post_tariff(tariff, session):
        new_tariff = Tariff(
            price=tariff.price,
            tariff_date=tariff.tariff_date,
        )
        session.add(new_tariff)
        await session.commit()
        await session.refresh(new_tariff)
        return {
            "id": new_tariff.id,
            "price": new_tariff.price,
            "tariff_date": new_tariff.tariff_date,
        } 

    async def update_tariff(id: int, tariff: TariffCreate, session):
        tariff_to_update = await session.get(Tariff, id)
        if tariff_to_update is None:
            raise HTTPException(status_code=404, detail=f"Нет тарифа с {id}, изменить невозможно")
        tariff_to_update.price = tariff.price
        tariff_to_update.tariff_date = tariff.tariff_date
        await session.commit()
        await session.refresh(tariff_to_update)
        return {
            "id": tariff_to_update.id,
            "price": tariff_to_update.price,
            "tariff_date": tariff_to_update.tariff_date,
        }

    async def delete_tariff(id: int, session):
        tariff_to_delete = await session.get(Tariff, id)
        if tariff_to_delete is None:
            raise HTTPException(status_code=404, detail=f"Нет тарифа с {id}, удалить невозможно")
        await session.delete(tariff_to_delete)
        await session.commit()
        return {"message": "Tariff deleted"}