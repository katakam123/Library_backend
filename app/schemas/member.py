from datetime import date
from pydantic import BaseModel, EmailStr, Field


class MemberCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)

    email: EmailStr

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        pattern=r"^[0-9+\-\s]+$"
    )

    address: str = Field(
        ...,
        min_length=1,
        max_length=300
    )

    membership_date: date

    is_active: bool = True


class MemberUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)

    email: EmailStr

    phone: str = Field(
        ...,
        min_length=10,
        max_length=15,
        pattern=r"^[0-9+\-\s]+$"
    )

    address: str = Field(
        ...,
        min_length=1,
        max_length=300
    )

    membership_date: date

    is_active: bool


class MemberResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    address: str
    membership_date: date
    is_active: bool

    class Config:
        from_attributes = True