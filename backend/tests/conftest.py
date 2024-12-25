import pytest
import asyncio
import json
from datetime import datetime
from sqlalchemy import insert
from database import Base, async_session
from config import MODE
from models.TariffModel import Tariff
from httpx import AsyncClient
from main import app


def open_testdata_json(filename):
    with open(f"backend/tests/testdata/{filename}.json", "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(scope="session", autouse=True)
async def prep_database():
    # test env
    print("mode: ", MODE)
    assert MODE == "TEST"

    # Database cleanup
    async with async_session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
        await session.close()
    
    # get testdata
    tariff = open_testdata_json("mock_tariff")

    for t in tariff:
        t["tariff_date"] = datetime.strptime(t["tariff_date"], "%Y-%m-%d").date()
        print(t)

    async with async_session() as session:
        data_to_add = [
            insert(Tariff).values(tariff)
        ]

        for command in data_to_add:
            await session.execute(command)
        await session.commit()
        await session.close()
    yield
    # clean up the test database at the end of tests
    # async with async_session() as session:
    #     for table in reversed(Base.metadata.sorted_tables):
    #         await session.execute(table.delete())
    #     await session.commit()
    #     await session.close()

@pytest.fixture(scope="session", autouse=True)
async def ac():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client
        client.aclose()