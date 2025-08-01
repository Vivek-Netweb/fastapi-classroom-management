import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def run():
    conn : asyncpg.Connection = await asyncpg.connect(DATABASE_URL)
    with open("migrations/005_alter_study_materials.sql", "r") as f:
        query = f.read()
    await conn.execute(query)
    print("Migration applied successfully.")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(run())