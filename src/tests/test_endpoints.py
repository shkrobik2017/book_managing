import pytest
import pytest_asyncio
import httpx
from fastapi import status


BASE_URL = "http://localhost:8081/v1/api/"


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        yield client


@pytest_asyncio.fixture
async def auth_token(client):
    user_data = {"username": "testuser", "password": "testpassword"}
    response = await client.post("/auth/token", data=user_data)
    return response.json()["access_token"]


@pytest.mark.asyncio()
async def test_register(client):
    user_data = {"username": "testuser", "password": "testpassword"}
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_invalid_register(client):
    user_data = {"username": "",}
    response = await client.post("/auth/register", json=user_data)
    assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio()
async def test_login(client):
    user_data = {"username": "testuser", "password": "testpassword"}
    response = await client.post("/auth/token", data=user_data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

@pytest.mark.asyncio()
async def test_invalid_login(client):
    user_data = {"password": ""}
    response = await client.post("/auth/token", data=user_data)
    assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio()
async def test_create_author(client, auth_token):
    author_data = {"name": "George", "surname": "Orwell", "birth_date": "1903-06-25", "biography": "English novelist"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post("/authors/create", json=author_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_invalid_create_author(client, auth_token):
    author_data = {"name": "George", "surname": "Orwell", "birth_date": "1565-06-25", "biography": "English novelist"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post("/authors/create", json=author_data, headers=headers)
    assert response.status_code != status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_get_all_authors(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get("/authors/all", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_get_author_by_id(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.get(f"/authors/{1}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_invalid_get_author_by_id(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.get(f"/authors/{"hi"}", headers=headers)
    assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio()
async def test_update_author(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    update_data = {"author_name": "Eric", "author_surname": "Blair"}
    response = await client.put(f"/authors/{1}", json=update_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_invalid_update_author(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    update_data = {"author_name": "Eric", "author_surname": "Blair"}
    response = await client.put(f"/authors/{"hi"}", json=update_data, headers=headers)
    assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio()
async def test_create_book(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    book_data = {"title": "1984", "author_id": 1, "published_year": 1949, "genre": "Fiction"}
    response = await client.post("/books/create", json=book_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_invalid_create_book(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    book_data = {"title": "1984", "author_id": 1, "published_year": 1454, "genre": "Fiction"}
    response = await client.post("/books/create", json=book_data, headers=headers)
    assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio()
async def test_import_books(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    with open("books.csv", "rb") as file:
        files = {"file": ("books.csv", file.read(), "text/csv")}
    response = await client.post("/books/import", files=files, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_invalid_import_books(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    with open("books.txt", "rb") as file:
        files = {"file": ("books.txt", file.read(), "text/txt")}
    response = await client.post("/books/import", files=files, headers=headers)
    assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio()
async def test_get_all_books(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.get("/books/all", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_get_book_by_id(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.get(f"/books/{1}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_invalid_get_book_by_id(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.get(f"/books/{"hi"}", headers=headers)
    assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio()
async def test_search_books(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.get("/books/search/", params={"title": "1984"}, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_update_book(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    update_data = {"book_title": "1984 (Updated)"}
    response = await client.put(f"/books/{1}", json=update_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_invalid_update_book(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    update_data = {"book_title": "1984 (Updated)", "book_published_year": 1454}
    response = await client.put(f"/books/{"hi"}", json=update_data, headers=headers)
    assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio()
async def test_delete_book(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.delete(f"/books/{1}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_delete_author(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.delete(f"/authors/{1}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True

@pytest.mark.asyncio()
async def test_invalid_delete_book(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.delete(f"/books/{1}", headers=headers)
    assert response.status_code != status.HTTP_200_OK

@pytest.mark.asyncio()
async def test_invalid_delete_author(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    response = await client.delete(f"/authors/{1}", headers=headers)
    assert response.status_code != status.HTTP_200_OK