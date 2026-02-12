import pytest
from httpx import AsyncClient
from app.models.user import User, UserRole
from app.security.hashing import hash_password

# Хелпер для создания пользователя в БД напрямую (минуя API)
async def create_user_in_db(db_session, email, role, uid):
    user = User(
        id=uid,
        email=email,
        hashed_password=hash_password("testpass"),
        role=role,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()

@pytest.mark.asyncio
async def test_admin_permissions_and_xss(client: AsyncClient, db_session, admin_token_headers, user_token_headers):
    # 1. Подготовка: Создаем в базе Админа (ID=1) и Юзера (ID=2)
    await create_user_in_db(db_session, "admin@test.com", UserRole.ADMIN, 1)
    await create_user_in_db(db_session, "user@test.com", UserRole.USER, 2)

    # 2. Тест: Обычный юзер пытается создать категорию (должен получить отказ)
    res = await client.post(
        "/api/v1/admin/categories", 
        json={"name": "Hacking", "slug": "hack"},
        headers=user_token_headers
    )
    assert res.status_code == 403  

    # 3. Тест: Админ создает категорию (должен быть успех)
    res = await client.post(
        "/api/v1/admin/categories", 
        json={"name": "Python", "slug": "python"},
        headers=admin_token_headers
    )
    assert res.status_code == 200
    category_id = res.json()["id"]

    # 4. Тест: Админ создает пост с XSS (проверка bleach)
    dangerous_content = "<h1>Title</h1><script>alert('xss')</script>"
    res = await client.post(
        "/api/v1/admin/posts",
        json={
            "title": "Security Test",
            "slug": "secure-post",
            "content_html": dangerous_content,
            "category_id": category_id
        },
        headers=admin_token_headers
    )
    assert res.status_code == 200

    res = await client.get("/api/v1/posts/secure-post")
    assert res.status_code == 200
    content = res.json()["content_html"]
    
    assert "<script>" not in content
    assert "&lt;script&gt;" in content or "alert" in content 