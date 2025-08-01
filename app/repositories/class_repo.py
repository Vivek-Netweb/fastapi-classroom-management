import asyncpg


class ClassRepository:
    def __init__(self, conn : asyncpg.Connection):
        self.conn = conn

    async def get_by_id(self, class_id : int):
        query = "SELECT * FROM classes WHERE id = $1"
        return await self.conn.fetchrow(query, class_id)
    
    async def get_class_by_teacher_id(self, teacher_id:int):
        query = "SELECT * FROM classes WHERE teacher_id = $1"
        return await self.conn.fetchrow(query, teacher_id)
        