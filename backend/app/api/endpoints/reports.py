from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
from typing import Optional
import csv
import io
from app.db.session import get_db
from app.models.models import User, Transaction, Category
from app.core.security import get_current_user

router = APIRouter()

@router.get("/data/")
async def get_report_data(start_date: Optional[str] = None, end_date: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get financial report data with category breakdown and monthly trends."""
    if not start_date:
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    query = select(Transaction).where(Transaction.user_id == current_user.id, Transaction.date >= start_date, Transaction.date <= end_date)
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    total_income = sum(float(t.amount) for t in transactions if t.type == "income")
    total_expenses = sum(float(t.amount) for t in transactions if t.type == "expense")
    
    category_result = await db.execute(select(Category).where(Category.user_id == current_user.id))
    categories = category_result.scalars().all()
    
    category_breakdown = []
    for cat in categories:
        amount = sum(float(t.amount) for t in transactions if t.category_id == cat.id)
        if amount > 0:
            total = total_income if cat.type == "income" else total_expenses
            percentage = round((amount / total) * 100, 1) if total > 0 else 0
            category_breakdown.append({"category": cat.name, "amount": amount, "percentage": percentage, "type": cat.type})
    
    monthly_trends = []
    for i in range(6):
        month_start = datetime.now().replace(day=1) - timedelta(days=30*i)
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_trans = [t for t in transactions if month_start.date() <= t.date <= month_end.date()]
        month_income = sum(float(t.amount) for t in month_trans if t.type == "income")
        month_expenses = sum(float(t.amount) for t in month_trans if t.type == "expense")
        
        monthly_trends.append({"month": month_start.strftime("%b %Y"), "income": month_income, "expenses": month_expenses, "net": month_income - month_expenses})
    
    monthly_trends.reverse()
    
    return {
        "totalIncome": total_income,
        "totalExpenses": total_expenses,
        "netBalance": total_income - total_expenses,
        "categoryBreakdown": category_breakdown,
        "monthlyTrends": monthly_trends,
        "incomeVsExpenses": monthly_trends
    }

@router.get("/export/")
async def export_transactions(start_date: Optional[str] = None, end_date: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Export transactions to CSV file."""
    query = select(Transaction, Category.name).join(Category, Transaction.category_id == Category.id, isouter=True).where(Transaction.user_id == current_user.id)
    
    if start_date:
        query = query.where(Transaction.date >= start_date)
    if end_date:
        query = query.where(Transaction.date <= end_date)
    
    result = await db.execute(query.order_by(Transaction.date.desc()))
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Description", "Category", "Type", "Amount"])
    
    for trans, cat_name in result.all():
        writer.writerow([trans.date, trans.description, cat_name or "Uncategorized", trans.type, trans.amount])
    
    output.seek(0)
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=transactions.csv"})
