from contextlib import asynccontextmanager
from app.db.database import Database
import asyncpg
from typing import AsyncGenerator

@asynccontextmanager
async def  get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    pool = Database.get_pool()
    conn  = await pool.acquire()
    print(f"✅ Acquired connection: {id(conn)}")
    try:
        yield conn
    finally:
        await Database.release_connection(conn)
        # print(f"🔁 Released connection: {id(conn)}")



async def get_conn_dependency() -> AsyncGenerator[asyncpg.Connection, None]:
    async with get_db_connection() as conn:
        yield conn