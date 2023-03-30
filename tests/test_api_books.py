def test_create_book(client):
    """Создаем книгу"""
    response = client.post(
        "api/books",
        json={"title": "Test Book Title"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Book Title"


def test_get_book_by_id(client):
    """Проверяем, доступна ли книга по ID"""
    response = client.post(
        "api/books",
        json={"title": "Book 1"},
    )
    assert response.status_code == 200, response.text
    response = client.get('api/books/1')
    assert response.status_code == 200, response.text


def test_edit_book(client):
    """Изменяем название книги"""
    response = client.post(
        "api/books",
        json={"title": "Title 1"},
    )
    response = client.get('api/books/1')
    assert response.status_code == 200, response.text
    response = client.put(
        "api/books",
        json={"id": 1, "title": "Title 2"},
    )
    response = client.get('api/books')
    data = response.json()[0]
    assert data["title"] == "Title 2"

    
def test_delete_book(client):
    """Удаляем книгу"""
    response = client.post(
        "api/books",
        json={"title": "TestTitle"},
    )
    assert response.status_code == 200, response.text
    response = client.delete(
        "api/books/1"
    )
    assert response.status_code == 200, response.text

