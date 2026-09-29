from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.book import Book
from app.models.member import Member
from app.models.borrow import BorrowRecord


def borrow_book(
    db: Session,
    book_id: int,
    member_id: int
):
    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    if not member.is_active:
        raise HTTPException(
            status_code=400,
            detail="Inactive members cannot borrow books"
        )

    if book.available_copies <= 0:
        raise HTTPException(
            status_code=400,
            detail="No copies available"
        )

    active_count = db.query(BorrowRecord).filter(
        BorrowRecord.member_id == member_id,
        BorrowRecord.return_date.is_(None)
    ).count()

    if active_count >= 3:
        raise HTTPException(
            status_code=400,
            detail="A member cannot borrow more than 3 books"
        )

    existing = db.query(BorrowRecord).filter(
        BorrowRecord.book_id == book_id,
        BorrowRecord.member_id == member_id,
        BorrowRecord.return_date.is_(None)
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Member already has this book"
        )

    borrow_date = date.today()
    due_date = borrow_date + timedelta(days=14)

    record = BorrowRecord(
        book_id=book_id,
        member_id=member_id,
        borrow_date=borrow_date,
        due_date=due_date,
        return_date=None,
        status="Borrowed"
    )

    book.available_copies -= 1

    db.add(record)
    db.commit()
    db.refresh(record)

    return record