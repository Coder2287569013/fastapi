from sqlalchemy.orm import Session
from db import models, schemas

def get_authors(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.DBAuthor).offset(skip).limit(limit).all()

def get_author(db: Session, author_id: int):
    return db.query(models.DBAuthor).filter(models.DBAuthor.id == author_id).first()

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.DBAuthor(name=author.name, second_name=author.second_name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)

    return db_author

def get_book(db: Session, name: str):
    return db.query(models.DBBook).filter(models.DBBook.name == name).first()

def get_books(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.DBBook).offset(skip).limit(limit).all()

def change_book(db: Session, name: str, new_name: str, new_pages: int):
    book = get_book(db = db, name = name)
    book.name = new_name
    book.pages = new_pages
    db.commit()

    return book

def delete_book(db: Session, name: str):
    db.query(models.DBBook).filter(models.DBBook.name == name).delete()
    db.commit()

def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.DBBook(name=book.name, pages=book.pages, author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.DBUser(login=user.login, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user(db: Session, login: str):
    return db.query(models.DBUser).filter(models.DBUser.login == login).first()