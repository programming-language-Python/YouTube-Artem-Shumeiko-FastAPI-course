import asyncio
import time

from fastapi import FastAPI, BackgroundTasks

app = FastAPI(title="My Base App")


def sync_task():
    time.sleep(3)
    print("Отправлен email")


async def async_task():
    await asyncio.sleep(3)
    print("Сделал запрос в сторонний API")


@app.post("/")
async def some_rout(bg_tasks: BackgroundTasks):
    ...
    # sync_task() # если даже заменить на async_task то всё равно будет выполняться 3 секунды
    asyncio.create_task(async_task())  # часто использующийся приём асинхронных функций, даже чаще чем BackgroundTasks
    bg_tasks.add_task(sync_task)
    return {"ok": True}  # сразу выполнится, не дожидаясь выше строчки
