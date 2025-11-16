from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.about import About
from app.schemas.about import AboutCreate, AboutUpdate


class AboutService:
    
    @staticmethod
    async def get(db: AsyncSession) -> About | None:
        """Получить информацию About (всегда одна запись)"""
        result = await db.execute(select(About).limit(1))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, about_data: AboutCreate) -> About:
        """Создать информацию About"""
        about = About(**about_data.model_dump())
        db.add(about)
        await db.commit()
        await db.refresh(about)
        return about
    
    @staticmethod
    async def update(
        db: AsyncSession,
        about_data: AboutUpdate
    ) -> About | None:
        """Обновить информацию About (обновляет первую запись)"""
        about = await AboutService.get(db)
        if not about:
            return None
        
        update_data = about_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(about, field, value)
        
        await db.commit()
        await db.refresh(about)
        return about
    
    @staticmethod
    async def delete(db: AsyncSession) -> bool:
        """Удалить информацию About"""
        about = await AboutService.get(db)
        if not about:
            return False
        
        await db.delete(about)
        await db.commit()
        return True