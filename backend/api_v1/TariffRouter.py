from fastapi import APIRouter, Depends
from typing import Annotated

from repositories.TariffRepositories import TariffRepositories
from schemas.TariffSchemas import Tariff, TariffCreate
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session


tariff_router = APIRouter(
    prefix="/api/v1",
    tags=["Tariff"],
)

@tariff_router.get("/tariff")
async def get_entity(session: AsyncSession = Depends(get_async_session)) -> list[Tariff]:
    """Get tariff."""
    result = await TariffRepositories.get_tariff(session)
    return result

@tariff_router.post("/tariff")
async def post_entity(tariff: Annotated[TariffCreate, Depends()], session: AsyncSession = Depends(get_async_session)) -> Tariff:
    """Post tariff."""
    result =  await TariffRepositories.post_tariff(tariff, session)
    return result

@tariff_router.put("/tariff/{id:int}")
async def update_entity(id, tariff: Annotated[Tariff, Depends()], session: AsyncSession = Depends(get_async_session)) -> Tariff:
    """Update tariff."""
    result = await TariffRepositories.update_tariff(id, tariff, session)
    return result

@tariff_router.delete("/tariff/{id:int}")
async def delete_entity(id: int, session: AsyncSession = Depends(get_async_session)):
    """Delete tariff."""
    result = await TariffRepositories.delete_tariff(id, session)
    return result