import uvicorn
from fastapi import FastAPI

app = FastAPI()


# root - в данном случае это ручка
# summary - меняет наименование ручки.
# tags - заменяет текст default.
@app.get("/", summary="Главная ручка", tags=['Основные ручки'])
def root():
    return 'hello world'


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
