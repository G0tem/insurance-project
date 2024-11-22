from fastapi import FastAPI
from backend.api_v1.Router import price_router


app = FastAPI()

app.include_router(price_router)