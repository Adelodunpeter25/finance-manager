from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List
from app.db.session import get_db
from app.models.models import User, Budget, Category
from app.schemas.schemas import Budget as BudgetSchema, BudgetCreate
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[BudgetSchema])
async def get_budgets(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all budgets for the current user."""
    result = await db.execute(select(Budget, Category.name).join(Category).where(Budget.user_id == current_user.id))
    return [{"id": b.id, "category_id": b.category_id, "amount": b.amount, "start_date": b.start_date, "end_date": b.end_date, "category_name": cn, "created_at": b.created_at} for b, cn in result.all()]

@router.post("/", response_model=BudgetSchema)
async def create_budget(budget: BudgetCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new budget."""
    db_budget = Budget(**budget.dict(), user_id=current_user.id)
    db.add(db_budget)
    await db.commit()
    await db.refresh(db_budget)
    
    result = await db.execute(select(Category.name).where(Category.id == db_budget.category_id))
    category_name = result.scalar_one_or_none()
    
    return {**db_budget.__dict__, "category_name": category_name}

@router.delete("/{budget_id}")
async def delete_budget(budget_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a budget."""
    result = await db.execute(select(Budget).where(and_(Budget.id == budget_id, Budget.user_id == current_user.id)))
    db_budget = result.scalar_one_or_none()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    await db.delete(db_budget)
    await db.commit()
    return {"message": "Budget deleted"}
