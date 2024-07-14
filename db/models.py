'''Creating tables for DB by using built-in classes and functions in module SQLAlchemy'''
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import relationship
from .engine import Base

class DBAuthor(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    second_name = Column(String(255), nullable=False)


class DBBook(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    pages = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor)

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)