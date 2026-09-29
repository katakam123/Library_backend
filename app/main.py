from fastapi import FastAPI

from app.database import Base, engine

from app.models.category import Category
from app.models.book import Book
from app.models.member import Member
from app.models.borrow import BorrowRecord

from app.routers import (
    categories,
    books,
    members,
    borrow
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Library Management API",
    description="FastAPI backend for Library Management",
    version="1.0.0"
)


app.include_router(categories.router)
app.include_router(books.router)
app.include_router(members.router)
app.include_router(borrow.router)


@app.get("/")
def root():
    return {
        "message": "Library Management API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }