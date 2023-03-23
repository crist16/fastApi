from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}
"""
@app.get('/')
async def getLibros(skip_book:str = "book_3"):
    new_books = BOOKS.copy()
    del new_books[skip_book]
    return new_books
"""

@app.get('/')
async def getLibro(the_book:str):
    return BOOKS[the_book]




@app.get('/books/{book_title}')
async def getLibro(book_title):
    return {
        "Message" : book_title
    }

@app.get('/{type_book}')
async def getLibroByName(type_book):
    return BOOKS[type_book]


