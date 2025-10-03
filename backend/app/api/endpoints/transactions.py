from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from app.db.session import get_db
from app.models.models import User, Transaction, Category
from app.schemas.schemas import Transaction as TransactionSchema, TransactionCreate, TransactionUpdate
from app.core.security import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TransactionSchema])
async def get_transactions(
    type: Optional[str] = None,
    category: Optional[int] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all transactions with optional filters."""
    query = select(Transaction, Category.name).join(Category, Transaction.category_id == Category.id, isouter=True).where(Transaction.user_id == current_user.id)
    
    if type:
        query = query.where(Transaction.type == type)
    if category:
        query = query.where(Transaction.category_id == category)
    if search:
        query = query.where(Transaction.description.ilike(f"%{search}%"))
    
    result = await db.execute(query.order_by(Transaction.date.desc()))
    return [{"id": t.id, "amount": t.amount, "type": t.type, "description": t.description, "date": t.date, "category_id": t.category_id, "category_name": cn, "created_at": t.created_at, "updated_at": t.updated_at} for t, cn in result.all()]

@router.post("/", response_model=TransactionSchema)
async def create_transaction(transaction: TransactionCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new transaction."""
    db_transaction = Transaction(**transaction.dict(), user_id=current_user.id)
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    
    category_name = None
    if db_transaction.category_id:
        result = await db.execute(select(Category.name).where(Category.id == db_transaction.category_id))
        category_name = result.scalar_one_or_none()
    
    return {**db_transaction.__dict__, "category_name": category_name}

@router.get("/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(transaction_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a specific transaction by ID."""
    result = await db.execute(select(Transaction, Category.name).join(Category, Transaction.category_id == Category.id, isouter=True).where(and_(Transaction.id == transaction_id, Transaction.user_id == current_user.id)))
    row = result.first()
    if not row:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {**row[0].__dict__, "category_name": row[1]}

@router.put("/{transaction_id}", response_model=TransactionSchema)
async def update_transaction(transaction_id: int, transaction_update: TransactionUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update an existing transaction."""
    result = await db.execute(select(Transaction).where(and_(Transaction.id == transaction_id, Transaction.user_id == current_user.id)))
    db_transaction = result.scalar_one_or_none()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    for key, value in transaction_update.dict(exclude_unset=True).items():
        setattr(db_transaction, key, value)
    
    await db.commit()
    await db.refresh(db_transaction)
    
    category_name = None
    if db_transaction.category_id:
        result = await db.execute(select(Category.name).where(Category.id == db_transaction.category_id))
        category_name = result.scalar_one_or_none()
    
    return {**db_transaction.__dict__, "category_name": category_name}

@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a transaction."""
    result = await db.execute(select(Transaction).where(and_(Transaction.id == transaction_id, Transaction.user_id == current_user.id)))
    db_transaction = result.scalar_one_or_none()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    await db.delete(db_transaction)
    await db.commit()
    return {"message": "Transaction deleted"}
