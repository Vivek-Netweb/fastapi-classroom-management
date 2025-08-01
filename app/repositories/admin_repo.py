from app.models.schemas.classes import ClassCreate
from app.models.schemas.subject import SubjectCreate
import asyncpg


class AdminRepository:
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    async def create_class(self, data: ClassCreate):
        query = "INSERT INTO classes (name, section) VALUES ($1,$2) RETURNING id, name, section"
        return await self.conn.fetchrow(query, data.name, data.section)

    async def get_class_by_id(self, class_id: int):
        query = "SELECT * FROM classes WHERE id = $1"
        return await self.conn.fetchrow(query, class_id)

    async def create_subject(self, data: SubjectCreate):
        query = "INSERT INTO subjects (name, class_id) VALUES ($1, $2) RETURNING id, name, class_id, created_at"
        return await self.conn.fetchrow(query, data.name, data.class_id)

    async def assign_teacher_to_class(self, teacher_id: int, class_id: int):
        query = "UPDATE classes SET teacher_id = $1 WHERE id = $2 RETURNING id, name, section, teacher_id"
        return await self.conn.fetchrow(query, teacher_id, class_id)
    
    async def get_all_teachers(self):
        # query = "SELECT * FROM users WHERE role='teacher'"
        query = "SELECT id,email,full_name FROM users WHERE role='teacher'"
        return await self.conn.fetch(query)

    async def get_all_classes(self):
        query = """
            SELECT 
                c.id AS class_id,
                c.name AS class_name,
                c.section,
                c.teacher_id,
                u.full_name AS teacher_name,
                u.email AS teacher_email,
                u.role AS teacher_role
            FROM public.classes c
            LEFT JOIN users u 
                ON c.teacher_id = u.id 
                AND u.role = 'teacher'
            ORDER BY c.id
        """
        return await self.conn.fetch(query)
