from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.interview_question import QuestionCategory
from app.schemas.interview_question import (
    InterviewQuestionCreate,
    InterviewQuestionUpdate,
    InterviewQuestionResponse,
)
from app.services.interview_question import InterviewQuestionService

router = APIRouter(prefix="/questions", tags=["Interview Questions"])


@router.get("/", response_model=list[InterviewQuestionResponse])
async def get_questions(
    category: QuestionCategory | None = None,
    difficulty: int | None = Query(None, ge=1, le=5),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Получить список вопросов к собеседованию"""
    questions = await InterviewQuestionService.get_all(
        db, category=category, difficulty=difficulty, skip=skip, limit=limit
    )
    return questions


@router.get("/{question_id}", response_model=InterviewQuestionResponse)
async def get_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Получить вопрос по ID"""
    question = await InterviewQuestionService.get_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.post("/", response_model=InterviewQuestionResponse, status_code=201)
async def create_question(
    question_data: InterviewQuestionCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создать новый вопрос"""
    question = await InterviewQuestionService.create(db, question_data)
    return question


@router.put("/{question_id}", response_model=InterviewQuestionResponse)
async def update_question(
    question_id: int,
    question_data: InterviewQuestionUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Обновить вопрос"""
    question = await InterviewQuestionService.update(db, question_id, question_data)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.delete("/{question_id}", status_code=204)
async def delete_question(
    question_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Удалить вопрос"""
    success = await InterviewQuestionService.delete(db, question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")