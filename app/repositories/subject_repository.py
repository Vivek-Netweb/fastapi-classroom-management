import asyncpg


class SubjectRepository:
    def __init__(self, conn : asyncpg.Connection):
        self.conn = conn

    async def get_subjects(self):
        query = """
    SELECT 
        s.id,
        s.name,
        s.class_id,
        s.created_at,
        c.name AS class_name,
        c.section AS class_section
    FROM subjects s
    JOIN classes c ON s.class_id = c.id
    ORDER BY s.id;
    """
        return await self.conn.fetch(query)