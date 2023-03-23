from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, Integer, String, ForeignKey
from sqlalchemy import create_engine



SQLALCHEMY_DATABASE_URL = "sqlite:///./datebase.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


class Book(Base):
    __tablename__ = "books"
 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genre = Column(String)
    author_id = Column(Integer, ForeignKey(Author.id))

   
Base.metadata.create_all(bind=engine)
 