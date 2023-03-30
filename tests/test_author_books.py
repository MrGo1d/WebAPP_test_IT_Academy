def test_create_author_book(client):
    """Создаем зависимость автор-книга"""
    response = client.post(
        "api/books",
        json={"title": "Test Book&Author"},
    )
    response = client.post(
        "api/authors",
        json={"name": "Test Name"},
    )
    assert response.status_code == 200, response.text
    response = client.post(
        "api/author_books",
        json={"auth_id": 1,
              "book_id": 1},
    )
    assert response.status_code == 200, response.text
