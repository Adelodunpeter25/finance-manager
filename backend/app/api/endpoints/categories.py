from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List
from app.db.session import get_db
from app.models.models import User, Category
from app.schemas.schemas import Category as CategorySchema, CategoryCreate
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CategorySchema])
async def get_categories(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all categories for the current user."""
    result = await db.execute(select(Category).where(Category.user_id == current_user.id).order_by(Category.name))
    return result.scalars().all()

@router.post("/", response_model=CategorySchema)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new category."""
    db_category = Category(**category.dict(), user_id=current_user.id)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

@router.delete("/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a category."""
    result = await db.execute(select(Category).where(and_(Category.id == category_id, Category.user_id == current_user.id)))
    db_category = result.scalar_one_or_none()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    await db.delete(db_category)
    await db.commit()
    return {"message": "Category deleted"}
