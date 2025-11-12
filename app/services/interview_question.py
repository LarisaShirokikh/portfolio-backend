from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.interview_question import InterviewQuestion, QuestionCategory
from app.schemas.interview_question import InterviewQuestionCreate, InterviewQuestionUpdate


class InterviewQuestionService:
    
    @staticmethod
    async def get_all(
        db: AsyncSession,
        category: QuestionCategory | None = None,
        difficulty: int | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> list[InterviewQuestion]:
        """Получить список вопросов с фильтрацией"""
        query = select(InterviewQuestion)
        
        if category:
            query = query.where(InterviewQuestion.category == category)
        if difficulty:
            query = query.where(InterviewQuestion.difficulty == difficulty)
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        return list(result.scalars().all())
    
    @staticmethod
    async def get_by_id(db: AsyncSession, question_id: int) -> InterviewQuestion | None:
        """Получить вопрос по ID"""
        result = await db.execute(
            select(InterviewQuestion).where(InterviewQuestion.id == question_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, question_data: InterviewQuestionCreate) -> InterviewQuestion:
        """Создать новый вопрос"""
        question = InterviewQuestion(**question_data.model_dump())
        db.add(question)
        await db.commit()
        await db.refresh(question)
        return question
    
    @staticmethod
    async def update(
        db: AsyncSession,
        question_id: int,
        question_data: InterviewQuestionUpdate
    ) -> InterviewQuestion | None:
        """Обновить вопрос"""
        question = await InterviewQuestionService.get_by_id(db, question_id)
        if not question:
            return None
        
        update_data = question_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(question, field, value)
        
        await db.commit()
        await db.refresh(question)
        return question
    
    @staticmethod
    async def delete(db: AsyncSession, question_id: int) -> bool:
        """Удалить вопрос"""
        question = await InterviewQuestionService.get_by_id(db, question_id)
        if not question:
            return False
        
        await db.delete(question)
        await db.commit()
        return True