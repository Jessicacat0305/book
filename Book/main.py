from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse

class NegativeNumberException(Exception):
    def __init__(self,books_to_return) :
        self.books_to_return = books_to_return

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length = 1)
    author: str = Field (min_length = 1, max_length = 100)
    description: Optional[str] = Field(title = "Description of the book", max_length = 100, min_length = 1)
    rating: int = Field(gt=-1, lt=101)

    #default
    class Config:
        schema_extra = {
            "example":{
            "id" : "9347fb09-d5ad-4b99-82e0-8fdf65eede26",
            "title" : "Computer Science Pro",
            "author" : "Codingwithroby",
            "description" : "A very nice description",
            "rating": 75
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(None, title="description of the Book", max_length=100, min_length = 1)


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negatiev_number_exception_handler(request: Request, exception: NegativeNumberException):
    
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, why do you want {exception.books_to_return}"
                 f"books? You need to read more!"}
    )

@app.post("/books/login/")
async def book_login(book_id: int, username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == "FastAPIUser" and password == "test1234!":
        return BOOKS[book_id]
    return "Invalid User"

@app.get("/header")
async def read_header(random_header: Optional[str]=Header (None)):
    return {"Random-Header": random_header}

@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):

    if books_to_return and books_to_return <0:
        raise NegativeNumberException(books_to_return=books_to_return)
    
    if len(BOOKS) < 1:
        create_books_no_api()

    if books_to_return and len(BOOKS)>= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i-1])
            i += 1
        return new_books
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id:UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()
        

@app.get("/book/rating/{book_id}", response_model=BookNoRating)
async def read_book_no_rating(book_id:UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.post("/", status_code = status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()

@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID: {book_id} deleted'
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id="6bbe830d-97db-4fb8-8cda-badc5fecd4e4", 
                  title = "Title 1",
                  author = "Author 1",
                  description = "Description 1",
                  rating = 60)
    book_2 = Book(id="d7132ad7-9b6c-434d-b7f9-477e6c438b82", 
                  title = "Title 2",
                  author = "Author 2",
                  description = "Description 2",
                  rating = 70)
    book_3 = Book(id="dacf38c9-3cab-4d78-a784-5036325482c8", 
                  title = "Title 3",
                  author = "Author 3",
                  description = "Description 3",
                  rating = 80)
    book_4 = Book(id="6c03ccf6-13c8-4096-9f89-30ccfdf3d4ed", 
                  title = "Title 4",
                  author = "Author 4",
                  description = "Description 4",
                  rating = 90)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={"X-header_Error":
                                  "Nothing to be seen at the UUID"})