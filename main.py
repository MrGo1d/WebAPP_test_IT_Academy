# """https://metanit.com/python/fastapi/1.15.php"""
from database import *
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import sessionmaker, Session
from base import engine, Book, Author
from sqlalchemy.ext.declarative import declarative_base




app = FastAPI()
 
# определяем зависимость
def get_db():
    Base = declarative_base()
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autoflush=False, bind=engine)
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
def get_author(id, db: Session = Depends(get_db)):
    # получаем пользователя по id
    author = db.query(Author).filter(Author.id == id).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if author==None:  
        return JSONResponse(status_code=404, content={ "message": f"[!] Автор c id = {id} не найден"})
    #если пользователь найден, отправляем его
    return author
  
  
@app.post("/api/authors")
def create_author(data = Body(), db: Session = Depends(get_db)):
    author = Author(name=data["name"])
    if db.query(Author).filter(Author.name == author.name).first():
        return JSONResponse(status_code=403, content={ "message": f"[!] Автор c именем '{author.name}' существует!"})
    else:
        db.add(author)
        db.commit()
        db.refresh(author)
    return author

@app.put("/api/authors")
def edit_author(data  = Body(), db: Session = Depends(get_db)):
   
    # получаем пользователя по id
    author = db.query(Author).filter(Author.id == data["id"]).first()
    # если не найден, отправляем статусный код и сообщение об ошибке
    if author == None: 
        return JSONResponse(status_code=404, content={ "message": "Пользователь не найден"})
    # если пользователь найден, изменяем его данные и отправляем обратно клиенту
    # person.age = data["age"]
    author.name = data["name"]
    db.commit() # сохраняем изменения 
    db.refresh(author)
    return author



@app.delete("/api/authors/{id}")
def delete_author(id, db: Session = Depends(get_db)):
    # получаем пользователя по id
    author = db.query(Author).filter(Author.id == id).first()
   
    # если не найден, отправляем статусный код и сообщение об ошибке
    if author == None:
        return JSONResponse( status_code=404, content={ "message": f"Автор с id = {id} не найден"})
   
    # если пользователь найден, удаляем его
    db.delete(author)  # удаляем объект
    db.commit()     # сохраняем изменения
    return author

# from sqlalchemy.orm import sessionmaker


# get_db()
# SessionLocal = sessionmaker(autoflush=False, bind=engine)
# db = SessionLocal()
# author_id = db.query(Author.id).filter(Author.name == 'Lev Tolstoy').first()[0]
# book = Book(title = 'Voina i mir tom 2', genre = 'Roman', author_id = author_id)

# if db.query(Book).filter(Book.title == book.title, Book.author_id == book.author_id).first():
#     print('Такая книга уже есть!')
# else:
#     db.add(book)     # добавляем в бд
#     db.commit()     # сохраняем изменения

