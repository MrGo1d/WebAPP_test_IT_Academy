import pytest
import sys
sys.path.append('c:\\Users\\a.ustinov\\Documents\\VSC\\IT Academy\\WebAPP_test_IT_Academy\\WebAPP_test_IT_Academy')
from fastapi.testclient import TestClient
from main import app, get_db
from database import Base, Author, Book, BookAuthor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///tests/test_datebase.db"


@pytest.fixture(scope="function")
def client():
    test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

    TestingSessionLocal = sessionmaker(autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    
    # Удаляем все данные из таблиц
    db = TestingSessionLocal()
    db.query(Book).delete()
    db.query(Author).delete()
    db.query(BookAuthor).delete()
    db.commit()
    db.close()

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client
