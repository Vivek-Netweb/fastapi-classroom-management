import asyncpg

class StudyMaterialRepository:
    def __init__(self, conn : asyncpg.Connection):
        self.conn = conn

    async def create(self,class_id : int, teacher_id:int,title : str, description : str, file_path : str, public_url : str):
        query = """
        INSERT INTO study_materials (class_id, teacher_id, title, description, file_path, public_url) 
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING *;
        """
        return await self.conn.fetchrow(query,class_id,teacher_id,title,description, file_path, public_url)

    async def get_by_class(self, class_id : int):
        query = "SELECT * FROM study_materials WHERE class_id = $1 ORDER BY uploaded_at DESC;" 
        return await self.conn.fetch(query, class_id)