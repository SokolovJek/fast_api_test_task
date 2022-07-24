from pydantic import BaseModel


class Token(BaseModel):
    """
    Валидация данных токена
    """
    access_token: str
    token_type: str
    refresh_token: str

