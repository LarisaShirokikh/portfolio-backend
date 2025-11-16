from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class AboutBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    bio: str = Field(..., min_length=1)
    photo_url: str | None = None
    resume_url: str | None = None
    
    email: EmailStr
    phone: str | None = None
    location: str | None = None
    
    github_url: str | None = None
    linkedin_url: str | None = None
    telegram_url: str | None = None
    
    years_of_experience: int = Field(default=0, ge=0)


class AboutCreate(AboutBase):
    pass


class AboutUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=255)
    title: str | None = None
    bio: str | None = None
    photo_url: str | None = None
    resume_url: str | None = None
    
    email: EmailStr | None = None
    phone: str | None = None
    location: str | None = None
    
    github_url: str | None = None
    linkedin_url: str | None = None
    telegram_url: str | None = None
    
    years_of_experience: int | None = Field(None, ge=0)


class AboutResponse(AboutBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}