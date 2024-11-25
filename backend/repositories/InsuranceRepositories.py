from schemas.InsuranceSchemas import InsuranceSchema
from sqlalchemy.ext.asyncio import AsyncSession
from models.InsuranceModel import Insurance


class InsuranceRepositories:
    """Class for insurance repositories."""
    @staticmethod
    async def post_insurance(insurance: InsuranceSchema, session: AsyncSession) -> None:
        return insurance