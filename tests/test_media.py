import io
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from PIL import Image

PET_DATA = {
    "name": "旺财",
    "species": "dog",
    "gender": "公",
    "age": 3,
}


def _make_test_image(size=(800, 600), fmt="JPEG") -> io.BytesIO:
    buf = io.BytesIO()
    img = Image.new("RGB", size, color="red")
    img.save(buf, format=fmt)
    buf.seek(0)
    return buf


@pytest.fixture
async def pet_id(client: AsyncClient) -> int:
    resp = await client.post("/pets", json=PET_DATA)
    return resp.json()["id"]


@pytest.mark.asyncio
async def test_upload_photo(client: AsyncClient, pet_id: int):
    image = _make_test_image()
    files = {"files": ("test.jpg", image, "image/jpeg")}
    response = await client.post(f"/pets/{pet_id}/media", files=files)
    assert response.status_code == 201
    data = response.json()
    assert len(data) == 1
    assert data[0]["media_type"] == "photo"
    assert data[0]["pet_id"] == pet_id
    assert data[0]["file_key"].endswith(".jpg")
    assert data[0]["thumbnail_key"] is not None
    assert data[0]["thumbnail_key"].endswith(".webp")
    assert data[0]["original_filename"] == "test.jpg"


@pytest.mark.asyncio
async def test_upload_photo_batch(client: AsyncClient, pet_id: int):
    img1 = _make_test_image()
    img2 = _make_test_image()
    files = [
        ("files", ("a.jpg", img1, "image/jpeg")),
        ("files", ("b.png", img2, "image/png")),
    ]
    response = await client.post(f"/pets/{pet_id}/media", files=files)
    assert response.status_code == 201
    data = response.json()
    assert len(data) == 2
    assert data[0]["original_filename"] == "a.jpg"
    assert data[1]["original_filename"] == "b.png"


@pytest.mark.asyncio
async def test_upload_unsupported_type(client: AsyncClient, pet_id: int):
    files = {"files": ("test.txt", b"hello world", "text/plain")}
    response = await client.post(f"/pets/{pet_id}/media", files=files)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_upload_pet_not_found(client: AsyncClient):
    image = _make_test_image()
    files = {"files": ("test.jpg", image, "image/jpeg")}
    response = await client.post("/pets/99999/media", files=files)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_media(client: AsyncClient, pet_id: int):
    image = _make_test_image()
    await client.post(f"/pets/{pet_id}/media", files={"files": ("p1.jpg", image, "image/jpeg")})
    response = await client.get(f"/pets/{pet_id}/media")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1
    assert data["items"][0]["pet_id"] == pet_id


@pytest.mark.asyncio
@patch("puppy_vacation_diary.routers.media.make_video_thumbnail", new_callable=AsyncMock)
async def test_upload_video(mock_thumb, client: AsyncClient, pet_id: int):
    fake_video = io.BytesIO(b"fake video content")
    files = {"files": ("clip.mp4", fake_video, "video/mp4")}
    response = await client.post(f"/pets/{pet_id}/media", files=files)
    assert response.status_code == 201
    data = response.json()
    assert len(data) == 1
    assert data[0]["media_type"] == "video"
    mock_thumb.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_media(client: AsyncClient, pet_id: int):
    image = _make_test_image()
    created = await client.post(f"/pets/{pet_id}/media", files={"files": ("del.jpg", image, "image/jpeg")})
    media_id = created.json()[0]["id"]

    response = await client.delete(f"/media/{media_id}")
    assert response.status_code == 204

    response = await client.get(f"/pets/{pet_id}/media")
    assert response.status_code == 200
    ids = [m["id"] for m in response.json()["items"]]
    assert media_id not in ids
