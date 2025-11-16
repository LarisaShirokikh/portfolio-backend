from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.interview_questions import router as questions_router
from app.api.v1.projects import router as projects_router 
from app.api.v1.about import router as about_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
)

# CORSы
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(questions_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1") 
app.include_router(about_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Portfolio Backend API",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}