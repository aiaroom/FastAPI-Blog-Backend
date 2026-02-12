import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_categories_empty(client: AsyncClient):
    # Проверяем, что публичный список категорий работает (должен быть пуст)
    response = await client.get("/api/v1/categories/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_category_posts_not_found(client: AsyncClient):
    # Проверяем 404 для несуществующего слага
    response = await client.get("/api/v1/categories/non-existent/posts")
    assert response.status_code == 404