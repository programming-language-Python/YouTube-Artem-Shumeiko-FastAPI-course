from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response

app = FastAPI()

# решение проблемы CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"]
    # какие сайты могут к нам обращаться. http://localhost:63342/ и http://127.0.0.1:63342/ это разные адреса. http и https тоже влияют
)

engine = create_async_engine("sqlite+aiosqlite:///books.db")

new_async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


# объявление БД
class BookModel(Base):
    __tablename__ = "books"  # можно называть во множественном числе или в единтственном, но выбрать один и всегда его придерживаться

    id: Mapped[int] = mapped_column(primary_key=True)  # обязательное иначе выдаст ошибку
    title: Mapped[str]
    author: Mapped[str]


class BookSchema(
    BaseModel):  # Schema - это Pydantic. Назвать можно как BookAddSchema, BookCreateSchema или BookPostSchema. Строгих соглашений нет
    title: str
    author: str


class BookGetSchema(BaseModel):
    id: int
    title: str
    author: str


# создание БД
@app.post("/setup_database")
async def setup_database():
    # открываем соединение с БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}


@app.post("/books")
async def add_books(data: BookSchema, session: SessionDep, response: Response):
    new_book = BookModel(
        title=data.title,
        author=data.author
    )
    # можно так
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:63342"
    session.add(new_book)
    await session.commit()
    return {"ok": True}


@app.get("/books")
async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()  # scalars чтоб не словить ошибки
