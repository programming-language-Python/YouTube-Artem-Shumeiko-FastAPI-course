from pydantic import BaseModel


class BookSchema(
    BaseModel):  # Schema - это Pydantic. Назвать можно как BookAddSchema, BookCreateSchema или BookPostSchema. Строгих соглашений нет
    title: str
    author: str


class BookGetSchema(BaseModel):
    id: int
    title: str
    author: str
