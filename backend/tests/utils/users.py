"""Мы собираемся хранить наши тестовые утилиты в этой папке(utils)"""
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from db.repository.users import create_new_user
from db.repository.users import get_user_by_email
from schemas.users import UserCreate


def user_authentication_headers(client: TestClient, email: str, password: str):
    """
    Создание заголовка с даными по токену
    """
    data = {'username': email, 'password': password}
    r = client.post('/login', data=data)
    response = r.json()
    auth_token = response['access_token']
    headers = {'Authorization': f'Bearer {auth_token}'}
    return headers


def authentication_token_from_email(client: TestClient, email: str, db: Session):
    """
    Возвращает действительный токен для пользователя с заданным email.
    Если пользователь не существует, он сначала создается.
    """
    password = 'random'
    user = get_user_by_email(email=email, db=db)
    if not user:
        user_in_create = UserCreate(username=email, email=email, password=password)
        user = create_new_user(user=user_in_create, db=db)
    return user_authentication_headers(client=client, email=email, password=password)
