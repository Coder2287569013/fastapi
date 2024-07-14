from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.engine import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/templates", StaticFiles(directory="templates"), name="template")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/img", StaticFiles(directory="img"), name="img")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def get_books(request: Request, db: Session = Depends(get_db)):
    data = crud.get_books(db=db)
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

@app.post("/user-create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/author-create/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.post("/{author_id}/book-create/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, author_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book, author_id=author_id)

@app.put("/{book_name}/get-book/", response_model=schemas.Book)
def change_book(name: str, new_info: schemas.BookCreate, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return crud.change_book(db=db, name=name, new_name=new_info.name, new_pages=new_info.pages)

@app.delete("/{book_name}/delete-book")
def delete_book(name: str, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    return crud.delete_book(db=db, name=name)

@app.post("/token")
async def token_create(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_data = crud.get_user(db=db, login=form_data.username)
    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password!")
    
    global user
    user = schemas.UserBase(login=user_data.login, password=user_data.password)