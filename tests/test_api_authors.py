import pytest


@pytest.mark.parametrize('link', ['/', 
                                  "/api/authors", 
                                  "/api/books", 
                                  "/api/author_books"
                                ])
def test_main_url(client, link):
    """Проверяем валидность всех ссылок"""
    response = client.get(link)
    assert response.status_code == 200


def test_create_author(client):
    """Создаем автора"""
    response = client.post(
        "api/authors",
        json={"name": "deadpool"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "deadpool"


def test_get_author_by_id(client):
    """Получаем автора по ID"""
    response = client.post(
        "api/authors",
        json={"name": "number 1"},
    )
    assert response.status_code == 200, response.text
    response = client.get('api/authors/1')
    assert response.status_code == 200, response.text


def test_edit_author(client):
    """Изменяем имя автора"""
    response = client.post(
        "api/authors",
        json={"name": "TestName 1"},
    )
    response = client.get('api/authors/1')
    assert response.status_code == 200, response.text
    response = client.put(
        "api/authors",
        json={"id": 1, "name": "TestName 2"},
    )
    response = client.get('api/authors')
    data = response.json()[0]
    assert data["name"] == "TestName 2"

    
def test_delete_author(client):
    """Удаляем автора"""
    response = client.post(
        "api/authors",
        json={"name": "TestName 1"},
    )
    assert response.status_code == 200, response.text
    client.delete(
        "api/authors/1"
    )
    response = client.get('api/authors/1')
    assert response.status_code == 404, response.text
