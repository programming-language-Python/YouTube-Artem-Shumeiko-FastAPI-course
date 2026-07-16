# импорт роутеров, чтоб использовать их в main.py. Роутеры могут использоваться в разных файлов (books, users) мы их переиновываем
from fastapi import APIRouter

from src.api.books import router as books_router

# from src.api.users import router as users_router
main_router = APIRouter()
main_router.include_router(books_router)
