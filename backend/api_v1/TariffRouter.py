from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.responses import JSONResponse

from repositories.TariffRepositories import TariffRepositories
from schemas.TariffSchemas import TariffSchema, UpdateTariffSchema
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session


tariff_router = APIRouter(
    prefix="/api/v1",
    tags=["Tariff"],
)

@tariff_router.get("/tariff/")
async def get_tariffs(session: AsyncSession = Depends(get_async_session)):
    try:
        tariffs = await TariffRepositories.get_tariffs(session)
        return tariffs
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@tariff_router.get("/tariff/{tariff_id}")
async def get_tariff(tariff_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        tariff = await TariffRepositories.get_tariff(tariff_id, session)
        return tariff
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@tariff_router.post("/tariff/")
async def post_tariff(tariff: Annotated[TariffSchema, Depends()], session: AsyncSession = Depends(get_async_session)):
    try:
        await TariffRepositories.post_tariff(tariff, session)
        return {"message": "JSON успешно загружен"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@tariff_router.put("/tariff/{tariff_id}")
async def update_tariff(tariff_id: int, tariff: Annotated[UpdateTariffSchema, Depends()], session: AsyncSession = Depends(get_async_session)):
    try:
        await TariffRepositories.update_tariff(tariff_id, tariff, session)
        return {"message": "Тариф успешно обновлен"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@tariff_router.delete("/tariff/{tariff_id}")
async def delete_tariff(tariff_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        await TariffRepositories.delete_tariff(tariff_id, session)
        return {"message": "Тариф успешно удален"}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
