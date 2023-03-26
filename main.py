# """https://metanit.com/python/fastapi/1.15.php"""
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from base import SessionLocal, Author, Book
from sqlalchemy.orm import Session


app = FastAPI()


# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return FileResponse("public/index.html")


@app.get("/api/authors")
def get_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()

  
@app.get("/api/authors/{id}")
def get_author(id: int, db: Session = Depends(get_db)):
    # получаем пользователя по id:создаем запрос в БД, в фильтре указываем полученный id пользователя
    author = db.query(Author).filter(Author.id == id).first()
    # если пользователь с таким ip не найден, отправляем статусный код и сообщение об ошибке
    if author is None:
        return JSONResponse(status_code=404, content={"message": f"[!] Автор c id = {id} не найден"})
    #если пользователь найден, возвращаем его
    return author
  
  
@app.post("/api/authors")
def create_author(name: str = Body(embed=True, min_length=2), db: Session = Depends(get_db)):
    # создаем объект АВТОР
    author = Author(name=name)
    # если автор с таким именем существует, отправляем статусный код и сообщение
    if db.query(Author).filter(Author.name == author.name).first():
        return JSONResponse(status_code=403, content={"message": f"[!] Автор c именем '{author.name}' существует!"})
    else:
        # если нет сохраняем данные в БД и обновляем базу
        db.add(author)
        db.commit()
        db.refresh(author)
    return author


@app.put("/api/authors")
def edit_author(id: int = Body(embed=True, gt=0), name: str = Body(embed=True, min_length=2), db: Session = Depends(get_db)):
    # получаем автора по id
    author = db.query(Author).filter(Author.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if author is None:
        return JSONResponse(status_code=404, content={"message": "[!] Автор не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    author.name = name
    # сохраняем изменения
    db.commit()
    db.refresh(author)
    return author


@app.delete("/api/authors/{id}")
def delete_author(id, db: Session = Depends(get_db)):
    # получаем пользователя по id
    author = db.query(Author).filter(Author.id == id).first()

    # если не найден, отправляем статусный код и сообщение об ошибке
    if author == None:
        return JSONResponse(status_code=404, content={"message": f"Автор с id = {id} не найден"})

    # если пользователь найден, удаляем его
    db.delete(author)  # удаляем объект
    db.commit()     # сохраняем изменения
    return author


@app.get("/api/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get("/api/books/{id}")
def get_book(id: int, db: Session = Depends(get_db)):
    # получаем книгу по id
    book = db.query(Book).filter(Book.id == id).first()
    # если не найдена, отправляем статусный код и сообщение об ошибке
    if book is None:
        return JSONResponse(status_code=404, content={"message": f"[!] Книга c id = {id} не найдена"})
    #если найдена, отправляем ее
    return book


@app.post("/api/books")
def create_book(title: str = Body(embed=True, min_length=2), db: Session = Depends(get_db)):
    book = Book(title=title)
    if db.query(Book).filter(Book.title == title).first():
        return JSONResponse(status_code=403, content={"message": f"[!] Книга c названием '{book.title}' уже существует!"})
    else:
        db.add(book)
        db.commit()
        db.refresh(book)
    return book


@app.put("/api/books")
def edit_book(id: int = Body(embed=True, gt=0), title: str = Body(embed=True, min_length=2), db: Session = Depends(get_db)):
    # получаем книгу по id
    book = db.query(Book).filter(Book.id == id).first()
    # если книга не найдена, отправляем статусный код и сообщение об ошибке
    if book is None: 
        return JSONResponse(status_code=404, content={"message": "[!] Книга не найдена"})
    # если книга найдена, изменяем ее данные и отправляем обратно клиенту
    book.title = title
    # сохраняем изменения
    db.commit()
    db.refresh(book)
    return book


@app.delete("/api/books/{id}")
def delete_book(id: int, db: Session = Depends(get_db)):
    # получаем книгу по id
    book = db.query(Book).filter(Book.id == id).first()
   
    # если не найдена, отправляем статусный код и сообщение об ошибке
    if book is None:
        return JSONResponse(status_code=404, content={"message": f"[!] Книга c названием '{book.title}' не найдена!"})
   
    # если найдена, удаляем ее
    db.delete(book)  # удаляем объект
    db.commit()     # сохраняем изменения
    db.refresh(book)
    return book


@app.post("/api/author_books")
def author_book(
        auth_id: int = Body(embed=True, gt=0),
        book_id: int = Body(embed=True, gt=0),
        db: Session = Depends(get_db)
):
    # находим автора и книгу по id
    author = db.query(Author).filter(Author.id == auth_id).first()
    book = db.query(Book).filter(Book.id == book_id).first()
    # проверяем наличие записи в базе
    if book.title in [book.title for book in author.books]:
        return JSONResponse(status_code=403, content={"message": f"[!] Книга c названием '{book.title}', {author.name} уже существует!"})
    author.books.append(book)
    db.commit()
    return author, book
