from typing import Literal
import pytest
import json
from httpx import AsyncClient
from tests.unit_tests.entity_tests.test_crud_api import BaseCrudTests
from src.models.CommentModel import Comment

class TestComment:
    @pytest.mark.parametrize("endpoint, param_id, respond_code", [
        ("/api/v1/comment", "100", 200),
        ("/api/v1/comment", "222", 404),
        # ("/api/v1/comment", "1000", 500)                     
    ])
    async def test_get_by_id(self, endpoint: str, param_id: str, respond_code: Literal[200], ac: AsyncClient):
        await BaseCrudTests.test_entity_get_by_id(endpoint, param_id, respond_code, ac)

    @pytest.mark.parametrize("endpoint, entity_model, ep_params, entry_name_to_find_by, respond_code", [
        ("/api/v1/comment", Comment,
      {
                "shift_id": 100,
                "text":  "тестовый коммент3",
                "is_pinned": True,
      }, "text", 401),
        ("/api/v1/comment", Comment,
      {
                "shift_id": 100,
                "text":  "тестовый коммент4",
                "is_pinned": False,
      }, "text", 401),
        ("/api/v1/comment", Comment,
      {
                "shift_id": 100,
                "text": "string",
                "is_pinned": False,
      }, "text", 401),
      
    ])
    async def test_create(self, endpoint: Literal['/api/v1/comment'], entity_model: Comment, ep_params: dict[str, int | str | list[int]], entry_name_to_find_by: Literal['name'], respond_code: Literal[200], ac: AsyncClient):
        await BaseCrudTests.test_entity_create(endpoint, entity_model, ep_params, entry_name_to_find_by, respond_code, ac)

    @pytest.mark.parametrize("endpoint, entity_model, ep_params, entity_id, entry_name_to_compare, respond_code", [
    ("/api/v1/comment", Comment,
      {
                "shift_id": 14,
                "text": "strИЗМЕНЕНingstrИЗМЕНЕНingstrИЗМЕНЕНingstrИЗМЕНЕНing",
                "is_pinned":  False
      }, 100, "text", 200),
    ("/api/v1/comment", Comment,
      {
                "shift_id": 14,
                "text": "strИЗМЕНЕНingstrИЗМЕНЕНingstrИЗМЕНЕНingstrИЗМЕНЕНing",
                "is_pinned":  False
      }, -1, "text", 500) 
    ])
    async def test_update_by_id(self, endpoint: Literal['/api/v1/comment'], entity_model: Comment, ep_params: dict[str, int | str | list[int]], entity_id: Literal[101] | Literal[-1], entry_name_to_compare: Literal['name'], respond_code: Literal[200] | Literal[500], ac: AsyncClient):
        await BaseCrudTests.test_entity_update_by_id(endpoint, entity_model, ep_params, entity_id, entry_name_to_compare, respond_code, ac)

    @pytest.mark.parametrize("endpoint, entity_model, entity_id, verify_delete, respond_code", [
        ("/api/v1/comment", Comment, 101, True, 200),
        ("/api/v1/comment", Comment, -1, True, 200)
    ])
    async def test_delete_by_id(self, endpoint, entity_model, entity_id, verify_delete, respond_code, ac: AsyncClient):
        await BaseCrudTests.test_entity_delete_by_id(endpoint, entity_model, entity_id, verify_delete, respond_code, ac)

    @pytest.mark.parametrize("endpoint, verify_count, respond_code", [
        ("/api/v1/comment", 1, 200)  
    ])
    async def test_get_all(self, endpoint, verify_count, respond_code, ac: AsyncClient):
        await BaseCrudTests.test_entity_get_all(endpoint, verify_count, respond_code, ac)