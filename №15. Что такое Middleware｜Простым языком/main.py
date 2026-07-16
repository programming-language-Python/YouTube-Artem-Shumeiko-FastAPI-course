import time
from typing import Callable

import uvicorn
from fastapi import FastAPI, Request, Response

app = FastAPI()


# # пустой middleware - ничего не делает
# @app.middleware("http")
# async def my_middleware(request: Request, call_next: Callable):
#     response = await call_next(request)
#     return response


@app.middleware("http")
async def my_middleware(request: Request, call_next: Callable):
    # ограничение запросов по пользователю
    ip_address = request.client.host  # дальше храним в redis и количество запросов пользователя
    print(f"{ip_address=}")
    # if ip_address in ["127.0.0.1", "localhost"]:
    #     return Response(status_code=429, content="Вы превысили кол-во запросов")

    start = time.perf_counter()
    response = await call_next(request)
    end = time.perf_counter() - start
    print(f"Время обработки запроса составило: {end}")  # в продакшене логируется, а не принтится
    # Можно проверять авторизацию пользователя. Если front-end прислал токен JWT можем проверить реально ли данный токен не экспонировался, какой user_id, является ли администратором, имеет ли доступ к ручке.
    response.headers["X-Special"] = "I am special"
    return response


@app.get("/users", tags=["Пользователи"])
async def get_users():
    time.sleep(0.5)
    return [{"id": 1, "name": "Artem"}]


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
