from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    tech_stack: str = Field(..., max_length=500)
    github_url: str | None = None
    demo_url: str | None = None
    image_url: str | None = None
    is_featured: bool = False
    order: int = 0


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    tech_stack: str | None = None
    github_url: str | None = None
    demo_url: str | None = None
    image_url: str | None = None
    is_featured: bool | None = None
    order: int | None = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}