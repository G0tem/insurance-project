import pytest
import json
from datetime import datetime
from sqlalchemy import insert
from database import Base, async_session_maker

from config import MODE
from models.TariffModel import Tariff


def open_testdata_json(filename):
    with open(f"backend/tests/testdata/{filename}.json", "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(scope="session", autouse=True)
def prep_database():
    print("mode: ", MODE)
    # test env
    assert MODE == "TEST"

    # Database cleanup
    with async_session_maker() as session:
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
        session.close()
    
    # get testdata
    tariff = open_testdata_json("mock_tariff")

    for t in tariff:
        t["tariff_date"] = datetime.strptime(t["tariff_date"], "%Y-%m-%d").date()
        print(t)

    with async_session_maker() as session:
        data_to_add = [
            insert(Tariff).values(tariff)
        ]

        for command in data_to_add:
            session.execute(command)
        session.commit()
        session.close()
    yield
    # clean up the test database at the end of tests
    # with async_session_maker() as session:
    #     for table in reversed(Base.metadata.sorted_tables):
    #         session.execute(table.delete())
    #     session.commit()
    #     session.close()
