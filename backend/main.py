from fastapi import FastAPI
from api_v1.TariffRouter import tariff_router
from api_v1.InsuranceRouter import insurance_router


app = FastAPI()

app.include_router(tariff_router)
app.include_router(insurance_router)