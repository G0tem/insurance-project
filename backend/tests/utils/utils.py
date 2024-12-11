from sqlalchemy import select
from fastapi.encoders import jsonable_encoder
from itertools import zip_longest
from database import async_session_maker


async def get_entity_by_entry(entity_model, entry_name, entry):
        session = async_session_maker()
        query = select(entity_model).where(getattr(entity_model, entry_name) == entry)
        exec_q = await session.execute(query)
        entity = exec_q.first()
        await session.close()
        if entity is None:
                return None
        entity = jsonable_encoder(entity[0])
        return entity

async def get_all_entities(entity_model):
        session = async_session_maker()
        query = select(entity_model)
        exec_q = await session.execute(query)
        entities = exec_q.scalars().all()
        await session.close()
        for i, entity in enumerate(entities):
                entities[i] = jsonable_encoder(entity)
        if entities is None:
                return None
        return entities

def compare_entities(ent_1, ent_2):
        paired = zip_longest(ent_1, ent_2, fillvalue="")
        return any(x != y for x, y in paired)