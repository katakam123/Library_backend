from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.member import Member
from app.models.borrow import BorrowRecord
from app.schemas.member import (
    MemberCreate,
    MemberUpdate,
    MemberResponse
)


router = APIRouter(
    prefix="/members",
    tags=["Members"]
)


@router.post(
    "",
    response_model=MemberResponse,
    status_code=201
)
def create_member(
    data: MemberCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Member).filter(
        Member.email == data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    member = Member(
        name=data.name,
        email=data.email,
        phone=data.phone,
        address=data.address,
        membership_date=data.membership_date,
        is_active=data.is_active
    )

    db.add(member)
    db.commit()
    db.refresh(member)

    return member


@router.get(
    "",
    response_model=list[MemberResponse]
)
def get_members(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return (
        db.query(Member)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get(
    "/{member_id}",
    response_model=MemberResponse
)
def get_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member


@router.put(
    "/{member_id}",
    response_model=MemberResponse
)
def update_member(
    member_id: int,
    data: MemberUpdate,
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    duplicate = db.query(Member).filter(
        Member.email == data.email,
        Member.id != member_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    member.name = data.name
    member.email = data.email
    member.phone = data.phone
    member.address = data.address
    member.membership_date = data.membership_date
    member.is_active = data.is_active

    db.commit()
    db.refresh(member)

    return member


@router.delete("/{member_id}")
def delete_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    active_borrow = db.query(BorrowRecord).filter(
        BorrowRecord.member_id == member_id,
        BorrowRecord.return_date.is_(None)
    ).first()

    if active_borrow:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete member with active borrowed books"
        )

    db.delete(member)
    db.commit()

    return {
        "message": "Member deleted successfully"
    }


@router.get(
    "/{member_id}/books"
)
def get_member_books(
    member_id: int,
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(
        Member.id == member_id
    ).first()

    if not member:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    records = db.query(BorrowRecord).filter(
        BorrowRecord.member_id == member_id,
        BorrowRecord.return_date.is_(None)
    ).all()

    return records