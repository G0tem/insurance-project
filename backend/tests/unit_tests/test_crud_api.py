import pytest
from httpx import AsyncClient
from sqlalchemy import select
import json
from database import async_session
from tests.utils.utils import *


class BaseCrudTests:
    @staticmethod
    async def test_entity_get_by_id(endpoint: str, param_id: str, respond_code, ac: AsyncClient):
        response = await ac.get(endpoint + '/' + param_id)
        assert response.status_code == respond_code
        if (respond_code == 200):
            data = json.loads(response.text)
            if (data == None):
                assert 0, "Got empty 200 response"
            if (int(data['id']) != int(param_id)):
                assert 0, "Got entity with wrong id"

    @staticmethod
    async def test_entity_create(endpoint, entity_model, ep_params, entry_name_to_find_by, respond_code,
                                 ac: AsyncClient):
        entities_old = await get_all_entities(entity_model)
        try:
            response = await ac.post(endpoint, json=ep_params)
        except:
            entities_new = await get_all_entities(entity_model)
            if (compare_entities(entities_old, entities_new)):
                assert 0, f"Data got modified after 500 error"
            assert 500 == respond_code
            return
        assert response.status_code == respond_code
        if (respond_code == 200):
            ent = await get_entity_by_entry(entity_model, entry_name_to_find_by, ep_params[entry_name_to_find_by])
            if ent is None:
                assert 0, f"Failed to find new entity {entity_model} in DB"
            elif ent[entry_name_to_find_by] != ep_params[entry_name_to_find_by]:
                assert 0, "Fetched wrong entity instead new one in DB"
        else:
            entities_new = await get_all_entities(entity_model)
            if (compare_entities(entities_old, entities_new) == True):
                assert 0, f"Data got modified after {response.status_code} error"

    @staticmethod
    async def test_entity_update_by_id(endpoint, entity_model, ep_params, entity_id, entry_name_to_compare,
                                       respond_code, ac: AsyncClient):
        ent_old = await get_entity_by_entry(entity_model, "id", entity_id)
        entities_old = await get_all_entities(entity_model)
        #if ent_old is None:
        #assert 0, f"Failed to find entity to update {entity_model} in DB"
        try:
            response = await ac.patch(endpoint + f"/{entity_id}", json=ep_params)
        except:
            entities_new = await get_all_entities(entity_model)
            if (compare_entities(entities_old, entities_new)):
                assert 0, f"Data got modified after 500 error"
            assert 500 == respond_code
            return
        assert response.status_code == respond_code
        if (response.status_code == 200):
            ent_new = await get_entity_by_entry(entity_model, "id", entity_id)
            if ent_new is None:
                assert 0, f"Failed to find new entity {entity_model} in DB"
            elif ent_old != None and ent_old[entry_name_to_compare] == ent_new[entry_name_to_compare]:
                assert 0, f"Failed to update entity {entity_model} in DB"
            elif ent_new[entry_name_to_compare] != ep_params[entry_name_to_compare]:
                assert 0, "Fetched wrong entity instead updated one in DB"

    @staticmethod
    async def test_entity_delete_by_id(endpoint, entity_model, entity_id, verify_delete, respond_code, ac: AsyncClient):
        if verify_delete:
            ent = await get_entity_by_entry(entity_model, "id", entity_id)
            #if ent is None:
            #assert 0, f"Failed to find entity to delete {entity_model} in DB"
        entities_old = await get_all_entities(entity_model)
        try:
            response = await ac.delete(endpoint + f"/{entity_id}")
        except:
            entities_new = await get_all_entities(entity_model)
            if (compare_entities(entities_old, entities_new)):
                assert 0, f"Data got modified after 500 error"
            assert 500 == respond_code
            return
        assert response.status_code == respond_code
        entities_new = await get_all_entities(entity_model)
        if (ent is None):
            if (compare_entities(entities_old, entities_new)):
                assert 0, f"Data got modified after trying to delete unexistent entity"
        if (verify_delete):
            ent_new = await get_entity_by_entry(entity_model, "id", entity_id)
            if ent_new is None:
                return
            else:
                assert 0, f"Failed to delete entity {entity_model} in DB"

    @staticmethod
    async def test_entity_get_all(endpoint, verify_count, respond_code, ac: AsyncClient):
        response = await ac.get(endpoint)
        assert response.status_code == respond_code
        if len(json.load(response)) != verify_count:
            assert 0, "Mismatched count of entities"

    @staticmethod
    async def test_entity_create_no_result(endpoint, entity_model, ep_params, entry_name_to_find_by, respond_code,
                                 ac: AsyncClient):
        entities_old = await get_all_entities(entity_model)
        try:
            response = await ac.post(endpoint, json=ep_params)
        except:
            entities_new = await get_all_entities(entity_model)
            if (compare_entities(entities_old, entities_new)):
                assert 0, f"Data got modified after 500 error"
            assert 500 == respond_code
            return
        assert response.status_code == respond_code

    @staticmethod
    async def test_entity_update_by_id_no_result(endpoint, entity_model, ep_params, entity_id, entry_name_to_compare,
                                       respond_code, ac: AsyncClient):
        ent_old = await get_entity_by_entry(entity_model, "id", entity_id)
        entities_old = await get_all_entities(entity_model)
        #if ent_old is None:
        #assert 0, f"Failed to find entity to update {entity_model} in DB"
        try:
            response = await ac.patch(endpoint + f"/{entity_id}", json=ep_params)
        except:
            entities_new = await get_all_entities(entity_model)
            if (compare_entities(entities_old, entities_new)):
                assert 0, f"Data got modified after 500 error"
            assert 500 == respond_code
            return
        assert response.status_code == respond_code