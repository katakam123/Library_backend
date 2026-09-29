from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.borrow import BorrowRecord
from app.models.book import Book
from app.models.member import Member
from app.schemas.borrow import (
    BorrowCreate,
    BorrowResponse
)
from app.services.borrow_service import borrow_book


router = APIRouter(
    tags=["Borrow & Return"]
)


@router.post(
    "/borrow",
    response_model=BorrowResponse,
    status_code=201
)
def create_borrow(
    data: BorrowCreate,
    db: Session = Depends(get_db)
):
    return borrow_book(
        db,
        data.book_id,
        data.member_id
    )


@router.put(
    "/return/{borrow_id}",
    response_model=BorrowResponse
)
def return_book(
    borrow_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(BorrowRecord).filter(
        BorrowRecord.id == borrow_id
    ).first()

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Borrow record not found"
        )

    if record.return_date is not None:
        raise HTTPException(
            status_code=400,
            detail="Book has already been returned"
        )

    today = date.today()

    record.return_date = today

    if today > record.due_date:
        record.status = "Overdue"
    else:
        record.status = "Returned"

    book = db.query(Book).filter(
        Book.id == record.book_id
    ).first()

    if book:
        book.available_copies += 1

        if book.available_copies > book.total_copies:
            book.available_copies = book.total_copies

    db.commit()
    db.refresh(record)

    return record


@router.get(
    "/books/{book_id}/borrow-history"
)
def get_book_history(
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

    records = db.query(BorrowRecord).filter(
        BorrowRecord.book_id == book_id
    ).order_by(
        BorrowRecord.borrow_date.desc()
    ).all()

    return records


@router.get(
    "/borrow/overdue"
)
def get_overdue_books(
    db: Session = Depends(get_db)
):
    records = db.query(BorrowRecord).filter(
        BorrowRecord.return_date.is_(None),
        BorrowRecord.due_date < date.today()
    ).all()

    for record in records:
        record.status = "Overdue"

    db.commit()

    return records