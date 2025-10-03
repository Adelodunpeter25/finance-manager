import asyncio
from app.db.session import AsyncSessionLocal
from app.models.models import User, UserRole
from app.core.security import get_password_hash

async def create_users():
    async with AsyncSessionLocal() as db:
        # Create admin user
        admin = User(
            username="admin",
            email="admin@financemanager.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            role=UserRole.admin,
            currency="USD",
            timezone="UTC"
        )
        db.add(admin)
        
        # Create regular user
        user = User(
            username="peter",
            email="adelodunpeter69@gmail.com",
            hashed_password=get_password_hash("peter123"),
            first_name="Peter",
            last_name="Adelodun",
            role=UserRole.user,
            currency="NGN",
            timezone="Africa/Lagos"
        )
        db.add(user)
        
        await db.commit()
        print("✅ Users created successfully!")
        print("\nAdmin credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("\nUser credentials:")
        print("  Username: peter")
        print("  Password: peter123")

if __name__ == "__main__":
    asyncio.run(create_users())
