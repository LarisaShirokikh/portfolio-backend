import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.interview_question import InterviewQuestion, QuestionCategory


async def seed_questions():
    """Заполнение БД тестовыми вопросами"""
    
    questions = [
        {
            "title": "Что такое GIL в Python?",
            "question": "Объясните, что такое Global Interpreter Lock (GIL) в Python и как он влияет на многопоточность.",
            "answer": "GIL (Global Interpreter Lock) - это механизм в CPython, который позволяет только одному потоку исполнять байт-код Python одновременно. Это упрощает управление памятью, но ограничивает многопоточность для CPU-bound задач. Для параллельного выполнения лучше использовать multiprocessing или asyncio.",
            "code_example": """# GIL ограничивает многопоточность
import threading
import time

def cpu_bound_task():
    count = 0
    for i in range(10_000_000):
        count += i

# Два потока не дадут прироста производительности на CPU-bound задачах
start = time.time()
t1 = threading.Thread(target=cpu_bound_task)
t2 = threading.Thread(target=cpu_bound_task)
t1.start()
t2.start()
t1.join()
t2.join()
print(f"Time: {time.time() - start}")""",
            "category": QuestionCategory.PYTHON,
            "difficulty": 3
        },
        {
            "title": "Async/await в Python",
            "question": "Как работают async/await в Python? В чем разница между асинхронным и многопоточным кодом?",
            "answer": "async/await - это синтаксис для работы с корутинами в Python. Асинхронный код использует одно ядро CPU и переключается между задачами во время ожидания I/O операций. Многопоточность использует несколько потоков ОС, но ограничена GIL.",
            "code_example": """import asyncio
import aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = ['https://example.com', 'https://example.org']
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

asyncio.run(main())""",
            "category": QuestionCategory.ASYNC,
            "difficulty": 4
        },
        {
            "title": "Dependency Injection в FastAPI",
            "question": "Как работает Dependency Injection в FastAPI?",
            "answer": "FastAPI использует Depends() для внедрения зависимостей. Это позволяет переиспользовать код, тестировать компоненты изолированно и управлять жизненным циклом ресурсов (например, БД сессиями).",
            "code_example": """from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()""",
            "category": QuestionCategory.FASTAPI,
            "difficulty": 3
        },
        {
            "title": "Индексы в PostgreSQL",
            "question": "Какие типы индексов существуют в PostgreSQL и когда их использовать?",
            "answer": "B-tree (по умолчанию, для сравнений), Hash (для точных совпадений), GiST (для геоданных), GIN (для полнотекстового поиска, массивов, JSON), BRIN (для больших таблиц с естественным порядком).",
            "code_example": """-- B-tree индекс
CREATE INDEX idx_user_email ON users(email);

-- Частичный индекс
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- Составной индекс
CREATE INDEX idx_user_name ON users(last_name, first_name);

-- GIN индекс для JSONB
CREATE INDEX idx_user_metadata ON users USING GIN(metadata);""",
            "category": QuestionCategory.DATABASES,
            "difficulty": 4
        },
        {
            "title": "Микросервисная архитектура",
            "question": "Назовите плюсы и минусы микросервисной архитектуры.",
            "answer": "Плюсы: независимое развертывание, масштабируемость отдельных сервисов, изоляция отказов, свобода выбора технологий. Минусы: сложность управления, распределенные транзакции, network latency, сложность отладки.",
            "code_example": None,
            "category": QuestionCategory.ARCHITECTURE,
            "difficulty": 4
        }
    ]
    
    async with AsyncSessionLocal() as db:
        for q_data in questions:
            question = InterviewQuestion(**q_data)
            db.add(question)
        
        await db.commit()
        print(f"✅ Добавлено {len(questions)} вопросов")


if __name__ == "__main__":
    asyncio.run(seed_questions())