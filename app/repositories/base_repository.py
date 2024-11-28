from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete

class BaseRepository:
    def __init__(self, db: AsyncSession, model):
        self.db = db
        self.model = model

    async def get_by_id(self, id: int):
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self):
        query = select(self.model)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, id: int, **kwargs):
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(query)
        await self.db.commit()
        return await self.get_by_id(id)

    async def delete(self, id: int):
        query = delete(self.model).where(self.model.id == id)
        await self.db.execute(query)
        await self.db.commit()
