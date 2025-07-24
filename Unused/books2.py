from fastapi import FastAPI,Path,Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date=published_date

class BookRequest(BaseModel):
    id: int | None = Field(description="ID is not needed on create",default=None)
    title: str =Field(min_length=3)
    author: str =Field(min_length=1)
    description: str =Field(min_length=1,max_length=100)
    rating: int =Field(gt=0, lt=6)
    published_date: int =Field(gt=1999,lt=2031)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"title",
                "author":"author",
                "description":"description",
                "rating":5,
                "published_date":2029,
            }
        }
    }

BOOKS =[
    Book(1, "Computer Science1","kim1", "description1", 1,2020),
    Book(2, "Computer Science2", "kim2", "description2", 2,2021),
    Book(3, "Computer Science3", "kim3", "description3", 3,2022),
    Book(4, "Computer Science4", "kim4", "description4", 4,2023),
    Book(5 ,"Computer Science5", "kim5", "description5", 5,2024),
]

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)#Path parameter
async def read_book(book_id: int=Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/",status_code=status.HTTP_200_OK)#Query parameter
async def read_book_by_rating(book_rating: int=Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/publish/",status_code=status.HTTP_200_OK)#Query parameter
async def read_books_by_publish_date(published_date: int=Query(gt=1999, lt=2030)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
        print(book)
    return books_to_return

@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump()) #**: Python의 unpacking 연산자 (딕셔너리의 키-값을 매개변수로 분해해서 전달)

    print(type(new_book))
    BOOKS.append(find_book_id(new_book))


def find_book_id(book:Book):
    book.id =1 if len(BOOKS) == 0 else BOOKS[-1].id +1
    return book

@app.put("/books/update-book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)#Path parameter
async def delete_book(book_id:int=Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")

