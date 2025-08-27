from fastapi import FastAPI

app=FastAPI()

#database
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]
#endpoints
@app.get("/")
async def checking_API():
    return{"message":"Hi, This is Ibraheem Shahzad"}

@app.get("/books")
async def get_books():
    return BOOKS

#to get one book or one specific thing we use path parameter
@app.get("/books/{book_title}")
async def book_title(book_title:str):
    for book in BOOKS:
        if book["title"].casefold()==book_title.casefold():
            return book
    return {"message":"book not found"}

#to get all the books related to something we use query paramter
@app.get("/books/")
async def books_category(category: str):
    books_by_category = []
    for book in BOOKS:
        if book["category"].casefold() == category.casefold():
            books_by_category.append(book)
    if books_by_category:
        return books_by_category
    return {"message": "Book category not found"}

@app.get("/books/{authorname}")
async def books_by_authors(authorname:str):
    books_by_author=[]
    for book in BOOKS:
        if book.get('author',"").casefold()==authorname.casefold():
            books_by_author.append(book)
    
    return books_by_author

@app.get("/books/{book_author}")
async def read_book_both(category:str, book_author:str):
    read_all=[]
    for book in BOOKS:
        if book.get("author","").casefold()==book_author.casefold() and book.get("category", "").casefold()==category.casefold():
            read_all.append(book)

    return read_all


@app.delete("/books/delete_book/{book_title}")
async def delete(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title","").casefold()==book_title.casefold():
            BOOKS.pop(i)
            break
        


