from fastapi import APIRouter
from sqlalchemy import select

from src.database import engine, Base
from src.models.books import BookModel
from src.schemas.books import BookSchema
# используем абсолютные импорты
from src.api.dependencies import SessionDep

router = APIRouter()  # если не имеем доступ к app (лежит в другом файле), то используется router вместо него


# создание БД

# тут идёт нарушение прицнипа DRY (не повторяйся) и тут не должно быть запросы к БД
@router.post("/setup_database")
async def setup_database():
    # открываем соединение с БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}


@router.post("/books")
async def add_books(data: BookSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True}


@router.get("/books")
async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()  # scalars чтоб не словить ошибки
