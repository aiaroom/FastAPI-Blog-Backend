import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post("/api/v1/auth/register", json={
        "email": "newuser@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@test.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "login@test.com",
        "password": "password123"
    })

    response = await client.post("/api/v1/auth/login", data={
        "username": "login@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={
        "email": "wrong@test.com",
        "password": "password123"
    })
    
    response = await client.post("/api/v1/auth/login", data={
        "username": "wrong@test.com",
        "password": "WRONGPASSWORD"
    })
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_refresh_token_endpoint(client: AsyncClient):
    await client.post("/api/v1/auth/register", json={"email": "refresh@test.com", "password": "password123"})
    login_res = await client.post("/api/v1/auth/login", data={"username": "refresh@test.com", "password": "password123"})
    token = login_res.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/api/v1/auth/refresh", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data