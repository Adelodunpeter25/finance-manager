import asyncio
from sqlalchemy import text
from app.db.session import engine

async def add_role_column():
    async with engine.begin() as conn:
        # Create enum type
        await conn.execute(text("""
            DO $$ BEGIN
                CREATE TYPE userrole AS ENUM ('user', 'admin');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """))
        
        # Add role column
        await conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS role userrole DEFAULT 'user' NOT NULL;
        """))
        
    print("✅ Role column added successfully!")

if __name__ == "__main__":
    asyncio.run(add_role_column())
