import asyncpg
from fastapi import Depends
from dotenv import load_dotenv
import os
from typing import Optional


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def connect(cls) -> asyncpg.Pool:
        if cls._pool is None:
            print("📡 Connecting to DB Pool...")
            cls._pool = await asyncpg.create_pool(DATABASE_URL)
        return cls._pool

    @classmethod
    async def disconnect(cls):
        if cls._pool is not None:
            print("❌ Closing DB Pool...")
            await cls._pool.close()
            cls._pool = None
            print("✅ Pool closed.")

    @classmethod
    async def release_connection(cls, conn: asyncpg.Connection):
        if cls._pool is not None:
            await cls._pool.release(conn)
            print(f"🔁 Released connection: {id(conn)}")

    @classmethod
    def get_pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            raise RuntimeError(
                "Database pool is not initialized. Call connect() first."
            )
        return cls._pool
