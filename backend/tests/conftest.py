"""конфигурации для тестирования"""
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import sys
import os

# это нужно для включения бэкенд директории в sys.path, чтобы мы могли импортировать(работать с) db, apis.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.base import Base
from db.session import get_db
from apis.base import api_router
from core.config import settings
from tests.utils.users import authentication_token_from_email


def start_application():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"

# {"check_same_thread": False} отключаем защиту от одновременного запроса к БД от разных потоков
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False}
                       )
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='function')
def app() -> Generator[FastAPI, Any, None]:
    """
    Создайте свежую базу данных для каждого тестового случая.
    """
    Base.metadata.create_all(engine)  # создает все таблици
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transactions = connection.begin()
    session = SessionTesting(bind=connection)
    yield session  # использовать сессию в тестах
    session.close()
    transactions.rollback()
    connection.close()


@pytest.fixture(scope='function')
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    """
    Создайте новый FastAPI TestClient, который использует фикстуру `db_session`, чтобы переопределить
    зависимость `get_db`, которая внедряется в маршруты.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='function')
def normal_user_token_headers(client: TestClient, db_session: Session):
    """
    Для получения действительного JWT токена.
    По сути, сделали функцию normal_user_token_header фикстурой на уровне модуля.
    Он будет вызван один раз для нашего варианта использования и даст нам токен jwt.
    """
    return authentication_token_from_email(client=client, email=settings.TEST_USER_EMAIL, db=db_session)
