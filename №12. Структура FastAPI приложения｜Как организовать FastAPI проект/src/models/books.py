from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.database import Base


# объявление БД
class BookModel(Base):
    __tablename__ = "books"  # можно называть во множественном числе или в единтственном, но выбрать один и всегда его придерживаться

    id: Mapped[int] = mapped_column(primary_key=True)  # обязательное иначе выдаст ошибку
    title: Mapped[str]
    author: Mapped[str]
