import pytest
from httpx import AsyncClient

PET_DATA = {
    "name": "旺财",
    "species": "dog",
    "gender": "公",
    "age": 3,
    "avatar": "https://example.com/avatar.jpg",
    "address": "北京市朝阳区",
    "birthday": "2022-03-15",
    "bio": "一只快乐的柯基",
}


@pytest.mark.asyncio
async def test_create_pet(client: AsyncClient):
    response = await client.post("/pets", json=PET_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == PET_DATA["name"]
    assert data["species"] == PET_DATA["species"]
    assert data["gender"] == PET_DATA["gender"]
    assert data["age"] == PET_DATA["age"]
    assert data["avatar"] == PET_DATA["avatar"]
    assert data["address"] == PET_DATA["address"]
    assert data["birthday"] == PET_DATA["birthday"]
    assert data["bio"] == PET_DATA["bio"]
    assert "id" in data
    return data


@pytest.mark.asyncio
async def test_list_pets(client: AsyncClient):
    await client.post("/pets", json=PET_DATA)
    response = await client.get("/pets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == PET_DATA["name"]


@pytest.mark.asyncio
async def test_get_pet(client: AsyncClient):
    created = await client.post("/pets", json=PET_DATA)
    pet_id = created.json()["id"]
    response = await client.get(f"/pets/{pet_id}")
    assert response.status_code == 200
    assert response.json()["name"] == PET_DATA["name"]


@pytest.mark.asyncio
async def test_get_pet_not_found(client: AsyncClient):
    response = await client.get("/pets/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_pet(client: AsyncClient):
    created = await client.post("/pets", json=PET_DATA)
    pet_id = created.json()["id"]
    response = await client.put(f"/pets/{pet_id}", json={"name": "小白", "age": 4})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "小白"
    assert data["age"] == 4
    assert data["species"] == PET_DATA["species"]


@pytest.mark.asyncio
async def test_delete_pet(client: AsyncClient):
    created = await client.post("/pets", json=PET_DATA)
    pet_id = created.json()["id"]
    response = await client.delete(f"/pets/{pet_id}")
    assert response.status_code == 204
    response = await client.get(f"/pets/{pet_id}")
    assert response.status_code == 404
