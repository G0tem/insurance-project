from fastapi import APIRouter, Depends
from typing import Annotated

from fastapi.responses import JSONResponse

from repositories.InsuranceRepositories import InsuranceRepositories
from schemas.InsuranceSchemas import InsuranceSchema
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session


insurance_router = APIRouter(
    prefix="/api/v1",
    tags=["Insurance"],
)

@insurance_router.post("/insurance")
async def post_insurance(insurance: Annotated[InsuranceSchema, Depends()], session: AsyncSession = Depends(get_async_session)):
    try:
        result = await InsuranceRepositories.post_insurance(insurance, session)
        return result
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
