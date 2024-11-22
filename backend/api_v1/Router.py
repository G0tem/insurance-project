from fastapi import APIRouter


price_router = APIRouter(
    prefix="/api/v1",
    tags=["Price"]
)


@price_router.get("/")
async def root():
    return {"message": "Hello World"}