from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.book import Book
from app.models.category import Category
from app.models.borrow import BorrowRecord
from app.schemas.book import (
    BookCreate,
    BookUpdate,
    BookResponse
)


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post(
    "",
    response_model=BookResponse,
    status_code=201
)
def create_book(
    data: BookCreate,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == data.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    if data.available_copies > data.total_copies:
        raise HTTPException(
            status_code=400,
            detail="Available copies cannot exceed total copies"
        )

    existing = db.query(Book).filter(
        Book.isbn == data.isbn
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="ISBN already exists"
        )

    book = Book(
        title=data.title,
        author=data.author,
        isbn=data.isbn,
        category_id=data.category_id,
        total_copies=data.total_copies,
        available_copies=data.available_copies,
        published_year=data.published_year
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book


@router.get(
    "",
    response_model=list[BookResponse]
)
def get_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None, gt=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    if title:
        query = query.filter(
            Book.title.ilike(f"%{title}%")
        )

    if author:
        query = query.filter(
            Book.author.ilike(f"%{author}%")
        )

    if category_id:
        query = query.filter(
            Book.category_id == category_id
        )

    return (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get(
    "/{book_id}",
    response_model=BookResponse
)
def get_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


@router.put(
    "/{book_id}",
    response_model=BookResponse
)
def update_book(
    book_id: int,
    data: BookUpdate,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    category = db.query(Category).filter(
        Category.id == data.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    if data.available_copies > data.total_copies:
        raise HTTPException(
            status_code=400,
            detail="Available copies cannot exceed total copies"
        )

    duplicate = db.query(Book).filter(
        Book.isbn == data.isbn,
        Book.id != book_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="ISBN already exists"
        )

    book.title = data.title
    book.author = data.author
    book.isbn = data.isbn
    book.category_id = data.category_id
    book.total_copies = data.total_copies
    book.available_copies = data.available_copies
    book.published_year = data.published_year

    db.commit()
    db.refresh(book)

    return book


@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    active_borrow = db.query(BorrowRecord).filter(
        BorrowRecord.book_id == book_id,
        BorrowRecord.return_date.is_(None)
    ).first()

    if active_borrow:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete a currently borrowed book"
        )

    db.delete(book)
    db.commit()

    return {
        "message": "Book deleted successfully"
    }