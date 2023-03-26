from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, Session


SQLALCHEMY_DATABASE_URL = "sqlite:///./datebase.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
# db = SessionLocal()

Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    books = relationship('Book', secondary='book_authors', back_populates='authors')


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    authors = relationship('Author', secondary='book_authors', back_populates='books')


class BookAuthor(Base):
    __tablename__ = "book_authors"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    book_id = Column(Integer, ForeignKey('books.id'))


SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
#


# with Session(bind=engine) as session:
#     usr1 = session.query(Author).filter(Author.id == 3).first()
#
# #     session.add(usr1)
# #
# #     session.commit()
# #
# #     # add projects
#     prj1 = Book(title="Kniga semena")
#     session.add(prj1)
#     session.commit()
# #
#     usr1.books.append(prj1)
# # #
#     session.commit()