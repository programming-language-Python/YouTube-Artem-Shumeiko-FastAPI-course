from fastapi import FastAPI, Depends, HTTPException, Response
from authx import AuthX, AuthXConfig

app = FastAPI(title="My Base App")

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


@app.post('/login')
def login(username: str, password: str, response: Response):
    if username == "test" and password == "test":
        token = security.create_access_token(
            uid=username)  # в нём хранятся данные, параметры их всегда может другой пользователь посмотреть (чувствительные данные, пароли нельзя)
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)  # чтоб сайт запомнил TOKEN
        return {"access_token": token}  # обычно называется так
    raise HTTPException(401, detail={"message": "Bad credentials"})


@app.get("/protected", dependencies=[Depends(
    security.access_token_required)])  # прописали что обязательно требуется токен, если его нет то код не выполнится
def get_protected():
    return {"message": "Hello World"}
