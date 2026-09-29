from typing import Optional

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    category_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    category_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    category_name: str
    description: Optional[str]

    class Config:
        from_attributes = True