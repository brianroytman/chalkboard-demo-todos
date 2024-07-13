import asyncio
from database import Base, engine

async def create_db():
    async with engine.begin() as conn:
        # Import your models here
        from models import Todo

        # Drop all tables if they exist
        print("Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)
        print("Tables dropped.")
        
        # Create all tables
        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created.")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_db())
