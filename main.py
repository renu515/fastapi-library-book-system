from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

# ---------------- DATA ----------------

books = [
    {"id": 1, "title": "Python Basics", "author": "John", "genre": "Tech", "is_available": True},
    {"id": 2, "title": "AI Guide", "author": "Smith", "genre": "Tech", "is_available": True},
    {"id": 3, "title": "History of India", "author": "Raj", "genre": "History", "is_available": True},
    {"id": 4, "title": "Science 101", "author": "Ravi", "genre": "Science", "is_available": True},
    {"id": 5, "title": "Fiction World", "author": "Anu", "genre": "Fiction", "is_available": True},
    {"id": 6, "title": "Data Science", "author": "Kiran", "genre": "Tech", "is_available": True}
]

borrow_records = []
queue = []
record_counter = 1

# ---------------- MODELS ----------------

class BorrowRequest(BaseModel):
    member_name: str = Field(..., min_length=2)
    book_id: int = Field(..., gt=0)
    borrow_days: int = Field(..., gt=0, le=30)
    member_id: str = Field(..., min_length=4)

class NewBook(BaseModel):
    title: str = Field(..., min_length=2)
    author: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=2)

# ---------------- HELPERS ----------------

def find_book(book_id):
    return next((b for b in books if b["id"] == book_id), None)

# ---------------- DAY 1 ----------------

@app.get("/")
def home():
    return {"message": "Welcome to Library"}

@app.get("/books")
def get_books():
    return {"books": books, "total": len(books)}

@app.get("/books/summary")
def summary():
    available = len([b for b in books if b["is_available"]])
    return {"total": len(books), "available": available}

# ---------------- DAY 2 + 3 ----------------

@app.post("/borrow")
def borrow(req: BorrowRequest):
    global record_counter

    book = find_book(req.book_id)
    if not book:
        raise HTTPException(404, "Book not found")

    if not book["is_available"]:
        return {"message": "Book not available"}

    book["is_available"] = False

    record = {
        "record_id": record_counter,
        "member_name": req.member_name,
        "book": book["title"]
    }

    record_counter += 1
    borrow_records.append(record)

    return record

@app.get("/books/filter")
def filter_books(genre: str = None):
    result = books
    if genre:
        result = [b for b in result if b["genre"] == genre]
    return {"books": result}

# ---------------- CRUD ----------------

@app.post("/books")
def add_book(book: NewBook):
    new_id = max(b["id"] for b in books) + 1
    new = book.dict()
    new["id"] = new_id
    new["is_available"] = True
    books.append(new)
    return new

@app.put("/books/{book_id}")
def update_book(book_id: int, is_available: bool = None):
    book = find_book(book_id)
    if not book:
        raise HTTPException(404, "Not found")

    if is_available is not None:
        book["is_available"] = is_available

    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(404, "Not found")

    books.remove(book)
    return {"message": "Deleted"}

# ---------------- WORKFLOW ----------------

@app.post("/queue/add")
def add_queue(member_name: str, book_id: int):
    queue.append({"member": member_name, "book_id": book_id})
    return {"message": "Added to queue"}

@app.post("/return/{book_id}")
def return_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(404, "Not found")

    book["is_available"] = True
    return {"message": "Returned"}
@app.get("/borrow-records")
def get_records():
    return {
        "borrow_records": borrow_records,
        "total": len(borrow_records)
    }

# ---------------- DAY 6 ----------------

@app.get("/books/search")
def search(keyword: str):
    result = [b for b in books if keyword.lower() in b["title"].lower()]
    return {"results": result}

@app.get("/books/sort")
def sort(sort_by: str = "title"):
    return {"books": sorted(books, key=lambda x: x[sort_by])}

@app.get("/books/page")
def page(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return {"books": books[start:start+limit]}

@app.get("/books/browse")
def browse(keyword: str = None, page: int = 1, limit: int = 2):
    result = books
    if keyword:
        result = [b for b in result if keyword.lower() in b["title"].lower()]
    start = (page - 1) * limit
    return {"books": result[start:start+limit]}