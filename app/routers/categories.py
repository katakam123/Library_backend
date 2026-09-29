from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.models.book import Book
from app.schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse
)


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=201
)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Category).filter(
        Category.category_name == data.category_name
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Category name already exists"
        )

    category = Category(
        category_name=data.category_name,
        description=data.description
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get(
    "",
    response_model=list[CategoryResponse]
)
def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return (
        db.query(Category)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.put(
    "/{category_id}",
    response_model=CategoryResponse
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    duplicate = db.query(Category).filter(
        Category.category_name == data.category_name,
        Category.id != category_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=409,
            detail="Category name already exists"
        )

    category.category_name = data.category_name
    category.description = data.description

    db.commit()
    db.refresh(category)

    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    book_exists = db.query(Book).filter(
        Book.category_id == category_id
    ).first()

    if book_exists:
        raise HTTPException(
            status_code=409,
            detail="Cannot delete category containing books"
        )

    db.delete(category)
    db.commit()

    return {
        "message": "Category deleted successfully"
    }