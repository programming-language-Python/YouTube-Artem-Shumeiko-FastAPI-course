from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, ConfigDict

app = FastAPI()

data = {
    "email": "abc@mail.ru",
    "bio": "Я пирожок",
    "age": 12,
}

data_wo_age = {
    "email": "abc@mail.ru",
    "bio": "Я пирожок",
    "age": 12,
    "gender": "male",
    "birthday": "2022"
}


class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=10)

    model_config = ConfigDict(extra='forbid')  # запрещает дополнительные поля


users = []


@app.post("/users")
def add_users(user: UserSchema):
    users.append(user)
    return {'ok': True, 'msg': 'Юзер добавлен'}


@app.get("/users")
def get_users() -> list[UserSchema]:
    return users


class UserAgeSchema(UserSchema):
    age: int = Field(ge=0, le=130)  # возраст от 0 до 130. ge - greater_than_equal, le - less_than_equal

# print(UserSchema(**data_wo_age))
# print(repr(UserAgeSchema(**data)))
