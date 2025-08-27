from typing import Optional
#for status
from fastapi import FastAPI, Path, Query, HTTPException, Body
#check for validation
from pydantic import BaseModel, Field
from starlette import status
#we can import this class rather that writing complete __init__ manually...
from dataclasses import dataclass



app = FastAPI()

#Dataclass
@dataclass #dataclass __ we will not have to write __init__ part
class Book:
    id : int
    title : str
    author : str
    description : str
    rating : int
    published_date : int

#this is used when we have to create or update a book
#this is know as PYDANTIC MODEL
#PYDANTIC MODEL is used when someone needs to update and apply chnages in complete BOOKS section like after finding 'id' complete BOOK section can be updated
class BookRequest(BaseModel):
    id : Optional[int]= Field(description ="ID is not neede n creatin",default=None)
    title: str = Field(min_length=3)
    description : str = Field(min_length=1, max_length=100)
    rating : int = Field(gt=0, lt=6)
    published_date : int = Field(gt=1999, lt=2031)


#database
BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


#endpoints/url's

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

#path parameter (used in to search specific oe thing)
@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def get_book_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
#query parameter (used in filter,catagory etc)
@app.get("/books",status_code=status.HTTP_200_OK)
async def books_by_rating(book_rating:int = Path(gt=0,lt=6)):
    books_by_rating=[]
    for book in BOOKS:
        if book.rating==book_rating:
            books_by_rating.append(book)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)  
    
#below function is used whwn we create a book or update a book below function is used to provide an id to it even if middle id is deleted it adjusts new book at the end


def find_new_book(book:Book):
    book.id=1 if len(BOOKS)==0 else BOOKS[-1].id+1
    return book

#double esteric is used like dictionary we have called pydantic model in function
@app.get("/books",status_code=status.HTTP_201_CREATED)
async def create_book(book_rquest:BookRequest):
    new_book=Book(**book_rquest.model_dump())
    BOOKS.append(find_new_book(new_book))

#Book is datamodel and BOOKS is database and BookRequest is Pydantic Model


#when i call book.reuqest.model_dump() it converts into dictionary

@app.put("/books/update_book", status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_request:BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_request.id:
            BOOKS[i]=Book(**book_request.model_dump())
            book_changed=True
    if not book_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Item not found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')




