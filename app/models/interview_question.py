from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import Enum

from app.core.database import Base


class QuestionCategory(str, Enum):
    PYTHON = "python"
    FASTAPI = "fastapi"
    DATABASES = "databases"
    ASYNC = "async"
    ARCHITECTURE = "architecture"
    ALGORITHMS = "algorithms"


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[str] = mapped_column(Text)
    code_example: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[QuestionCategory] = mapped_column(SQLEnum(QuestionCategory))
    difficulty: Mapped[int] = mapped_column(default=1)  # 1-5
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)