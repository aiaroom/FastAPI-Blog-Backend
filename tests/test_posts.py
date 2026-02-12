import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_posts_empty(client: AsyncClient):
    # Проверяем публичный список постов
    response = await client.get("/api/v1/posts/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_single_post_404(client: AsyncClient):
    # Проверяем 404 для поста
    response = await client.get("/api/v1/posts/not-found")
    assert response.status_code == 404