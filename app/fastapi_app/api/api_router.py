
from fastapi import APIRouter

from app.fastapi_app.api.v1 import v1_router

api_router = APIRouter()
api_router.include_router(v1_router.router, tags=['Ручка для метрик пользователя'])
