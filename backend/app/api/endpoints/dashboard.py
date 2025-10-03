from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.db.session import get_db
from app.models.models import User, Transaction, Budget, Category
from app.schemas.schemas import DashboardStats, RecentTransaction, BudgetStatus
from app.core.security import get_current_user

router = APIRouter()

@router.get("/stats/", response_model=DashboardStats)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get financial statistics for dashboard."""
    income_result = await db.execute(select(func.sum(Transaction.amount)).where(Transaction.user_id == current_user.id, Transaction.type == "income"))
    income = float(income_result.scalar() or 0)
    
    expense_result = await db.execute(select(func.sum(Transaction.amount)).where(Transaction.user_id == current_user.id, Transaction.type == "expense"))
    expense = float(expense_result.scalar() or 0)
    
    budget_result = await db.execute(select(func.sum(Budget.amount)).where(Budget.user_id == current_user.id))
    total_budget = float(budget_result.scalar() or 0)
    
    return {
        "totalIncome": income,
        "totalExpenses": expense,
        "netBalance": income - expense,
        "budgetUtilization": round((expense / total_budget) * 100, 1) if total_budget > 0 else 0
    }

@router.get("/recent-transactions/", response_model=List[RecentTransaction])
async def get_recent_transactions(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get 5 most recent transactions."""
    result = await db.execute(select(Transaction, Category.name).join(Category, Transaction.category_id == Category.id, isouter=True).where(Transaction.user_id == current_user.id).order_by(Transaction.date.desc()).limit(5))
    return [{"id": t.id, "amount": float(t.amount), "type": t.type, "category": cn or "Uncategorized", "date": t.date.strftime("%Y-%m-%d"), "description": t.description} for t, cn in result.all()]

@router.get("/budget-status/", response_model=List[BudgetStatus])
async def get_budget_status(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get budget progress for all active budgets."""
    result = await db.execute(select(Budget, Category.name).join(Category).where(Budget.user_id == current_user.id))
    budgets = []
    
    for budget, cat_name in result.all():
        spent_result = await db.execute(select(func.sum(Transaction.amount)).where(Transaction.user_id == current_user.id, Transaction.category_id == budget.category_id, Transaction.type == "expense", Transaction.date >= budget.start_date, Transaction.date <= budget.end_date))
        spent = float(spent_result.scalar() or 0)
        percentage = round((spent / float(budget.amount)) * 100, 1) if budget.amount > 0 else 0
        
        budgets.append({"id": budget.id, "category": cat_name, "budgetAmount": float(budget.amount), "spentAmount": spent, "percentage": percentage})
    
    return budgets
