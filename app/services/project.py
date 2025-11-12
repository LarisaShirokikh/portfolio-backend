from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        is_featured: bool | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> list[Project]:
        """Получить список проектов"""
        query = select(Project).order_by(Project.order.desc(), Project.created_at.desc())
        
        if is_featured is not None:
            query = query.where(Project.is_featured == is_featured)
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def get_by_id(db: AsyncSession, project_id: int) -> Project | None:
        """Получить проект по ID"""
        result = await db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, project_data: ProjectCreate) -> Project:
        """Создать новый проект"""
        project = Project(**project_data.model_dump())
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project
    
    @staticmethod
    async def update(
        db: AsyncSession,
        project_id: int,
        project_data: ProjectUpdate
    ) -> Project | None:
        """Обновить проект"""
        project = await ProjectService.get_by_id(db, project_id)
        if not project:
            return None
        
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        
        await db.commit()
        await db.refresh(project)
        return project
    
    @staticmethod
    async def delete(db: AsyncSession, project_id: int) -> bool:
        """Удалить проект"""
        project = await ProjectService.get_by_id(db, project_id)
        if not project:
            return False
        
        await db.delete(project)
        await db.commit()
        return True