from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.about import (
    AboutCreate,
    AboutUpdate,
    AboutResponse,
)
from app.services.about import AboutService

router = APIRouter(prefix="/about", tags=["About"])


@router.get("/", response_model=AboutResponse)
async def get_about(
    db: AsyncSession = Depends(get_db),
):
    """Получить информацию обо мне"""
    about = await AboutService.get(db)
    if not about:
        raise HTTPException(status_code=404, detail="About info not found")
    return about


@router.post("/", response_model=AboutResponse, status_code=201)
async def create_about(
    about_data: AboutCreate,
    db: AsyncSession = Depends(get_db),
):
    """Создать информацию обо мне (только одна запись)"""
    # Проверяем, что запись еще не существует
    existing = await AboutService.get(db)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="About info already exists. Use PUT to update."
        )
    
    about = await AboutService.create(db, about_data)
    return about


@router.put("/", response_model=AboutResponse)
async def update_about(
    about_data: AboutUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Обновить информацию обо мне"""
    about = await AboutService.update(db, about_data)
    if not about:
        raise HTTPException(status_code=404, detail="About info not found")
    return about


@router.delete("/", status_code=204)
async def delete_about(
    db: AsyncSession = Depends(get_db),
):
    """Удалить информацию обо мне"""
    success = await AboutService.delete(db)
    if not success:
        raise HTTPException(status_code=404, detail="About info not found")