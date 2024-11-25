from fastapi import FastAPI
from api_v1.TariffRouter import tariff_router


app = FastAPI()

app.include_router(tariff_router)