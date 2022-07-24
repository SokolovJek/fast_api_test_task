"""Главный машрутизатор в котором будут хранится все маршруты"""

from fastapi import APIRouter

from apis.version1 import route_users, route_authenticated, route_general_pages

api_router = APIRouter()
api_router.include_router(route_general_pages.general_pages_router, prefix='', tags=['general_pages'])
api_router.include_router(route_users.router, prefix='/user', tags=['user'])
api_router.include_router(route_authenticated.router, prefix='', tags=['login_and_logout'])

