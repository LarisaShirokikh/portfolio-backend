from pydantic import BaseModel, Field
from datetime import datetime
from app.models.interview_question import QuestionCategory


class InterviewQuestionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
    code_example: str | None = None
    category: QuestionCategory
    difficulty: int = Field(default=1, ge=1, le=5)


class InterviewQuestionCreate(InterviewQuestionBase):
    pass


class InterviewQuestionUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    question: str | None = Field(None, min_length=1)
    answer: str | None = Field(None, min_length=1)
    code_example: str | None = None
    category: QuestionCategory | None = None
    difficulty: int | None = Field(None, ge=1, le=5)


class InterviewQuestionResponse(InterviewQuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}