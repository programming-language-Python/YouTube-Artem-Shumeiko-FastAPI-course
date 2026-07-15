# Юнит тест
# def func(num: int):
#     return 1 / num
#
#
# def test_func():
#     assert func(1) == 1
#     assert func(2) == 0.5
#     # assert func(0)
import pytest
from httpx import AsyncClient, ASGITransport

from main import app


# Интеграционные тесты
@pytest.mark.asyncio  # обязательно для асинхронных тестов, чтобы грамотно обработалась плагином asyncio
async def test_get_books():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"  # обычно так называют
    ) as ac:
        response = await ac.get("/books")
        assert response.status_code == 200
        # print(response)
        data = response.json()
        assert len(data) == 2


# принцип DRY тут опущен (не повторяйся)
@pytest.mark.asyncio  # обязательно для асинхронных тестов, чтобы грамотно обработалась плагином asyncio
async def test_post_books():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"  # обычно так называют
    ) as ac:
        response = await ac.post("/books", json={
            "title": "Nazvanie",
            "author": "Author"
        })
        assert response.status_code == 200
        # print(response)
        data = response.json()
        assert len(data) == 2
