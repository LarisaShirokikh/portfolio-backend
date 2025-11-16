from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.core.database import Base


class About(Base):
    __tablename__ = "about"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))  # "Senior Backend Developer"
    bio: Mapped[str] = mapped_column(Text)  # Краткое описание
    photo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resume_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    # Контакты
    email: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # Социальные сети
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    telegram_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    years_of_experience: Mapped[int] = mapped_column(default=0)
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)