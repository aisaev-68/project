from fastapi import APIRouter

from app.api.v1.endpoints import upload, export, chat_data

api_router = APIRouter()
api_router.include_router(upload.router, prefix="/api/upload", tags=["Загрузка файла"])
api_router.include_router(export.router, prefix="/api/export", tags=["Выгрузка файла"])
api_router.include_router(chat_data.router, prefix="/api/chat_data", tags=["Данные для диаграммы"])