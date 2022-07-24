from pydantic import BaseModel, EmailStr
from typing import Optional


# указываем свойства, необходимые при создании пользователя.
class UserCreate(BaseModel):
    """
    Валидация данных
    """
    username: str
    email: EmailStr
    password: str


# модель ответа сервера на запрос 'POST http://127.0.0.1:8000/users/{id_user}'
class ShowUser(BaseModel):
    """
    Явно указываем что будет возвращенно пользователю.
    Убираем и ответа поля: hash_password и is_superuser
    """
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
