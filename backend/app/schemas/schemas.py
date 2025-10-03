from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    currency: str = "NGN"
    timezone: str = "UTC"
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    currency: Optional[str] = None

class Token(BaseModel):
    access: str
    refresh: str
    user: User

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    type: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Transaction Schemas
class TransactionBase(BaseModel):
    amount: Decimal = Field(gt=0)
    type: str
    description: Optional[str] = ""
    date: date
    category_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    type: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None
    category_id: Optional[int] = None

class Transaction(TransactionBase):
    id: int
    category_name: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Budget Schemas
class BudgetBase(BaseModel):
    category_id: int
    amount: Decimal = Field(gt=0)
    start_date: date
    end_date: date

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    category_name: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardStats(BaseModel):
    totalIncome: float
    totalExpenses: float
    netBalance: float
    budgetUtilization: float

class RecentTransaction(BaseModel):
    id: int
    amount: float
    type: str
    category: str
    date: str
    description: str

class BudgetStatus(BaseModel):
    id: int
    category: str
    budgetAmount: float
    spentAmount: float
    percentage: float
