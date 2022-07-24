from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.config import settings
from apis.base import api_router
from db.session import engine
from db.base import Base

from db.black_list import init_blacklist_file


def include_router(my_app):
    my_app.include_router(api_router)


def configure_static(my_app):
    """Сообщаем FastAPI что статика хранится в директории 'static' """
    # name='static' для того чтоб Jinja2 мог найти его
    my_app.mount('/static', StaticFiles(directory='static'), name='static')


def create_tables():
    print("ТАБЛИЦЫ СОЗДАНЫ :)")
    Base.metadata.create_all(bind=engine)


def start_applications():
    my_app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(my_app)
    configure_static(my_app)
    create_tables()
    return my_app


# реализация blacklist для end-point /logout
# init_blacklist_file()
app = start_applications()
