import asyncio
import threading
import time

import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

hotels = [
    {
        "id": 1,
        "title": "Sochi",
        "name": "sochi",
    },
    {
        "id": 2,
        "title": "Дубай",
        "author": "dubai",
    }
]


@app.get("/test")
async def test():
    await asyncio.gather(
        *[get_data(i, "async") for i in range(20)]
    )


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Потоков: {threading.active_count()}")
    print(f"async. Начал {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time():.2f}")


def get_data(id: int, name: str):
    exec(f"await {name}_func({id})")


if __name__ == '__main__':
    uvicorn.run('main:app', workers=1)
