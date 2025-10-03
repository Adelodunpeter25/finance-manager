from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserLogin, Token, User as UserSchema, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, get_current_user

router = APIRouter()

@router.post("/register/", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user and return JWT tokens."""
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = User(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return {
        "access": create_access_token({"sub": user.id}),
        "refresh": create_refresh_token({"sub": user.id}),
        "user": user
    }

@router.post("/login/", response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """Authenticate user and return JWT tokens."""
    result = await db.execute(select(User).where(User.username == credentials.username))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {
        "access": create_access_token({"sub": user.id}),
        "refresh": create_refresh_token({"sub": user.id}),
        "user": user
    }

@router.get("/user/", response_model=UserSchema)
async def get_user(current_user: User = Depends(get_current_user)):
    """Get current authenticated user profile."""
    return current_user

@router.put("/user/", response_model=UserSchema)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user profile."""
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/logout/")
async def logout():
    """Logout user."""
    return {"message": "Logout successful"}
