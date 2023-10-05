import datetime
from typing import Optional, List
from datetime import date
from pydantic import BaseModel


class Value(BaseModel):
    year: int
    plan_value: float
    fact_value: float


class Project(BaseModel):
    name: str
    version_id: int


class ChatDataPlan(BaseModel):
    name: str
    version_id: int
    year: int
    plan_value: float

    class Config:
        from_attributes = True


class ChatDataFact(BaseModel):
    name: str
    version_id: int
    year: int
    fact_value: float

    class Config:
        from_attributes = True


class DataListPlan(BaseModel):
    projects: List[ChatDataPlan]

    class Config:
        json_schema_extra = {
            'title': 'DataListPlan',
            'description': 'Example DataListPlan list',
            'example': [
                {
                    'name': '',
                    'version_id': 1,
                    'year': 2022,
                    'plan_value': 12.23
                },
            ]
        }


class DataListFact(BaseModel):
    projects: List[ChatDataFact]

    class Config:
        json_schema_extra = {
            'title': 'DataListFact',
            'description': 'Example DataListFact list',
            'example': [
                {
                    'name': '',
                    'version_id': 1,
                    'year': 2022,
                    'fact_value': 12.23
                },
            ]
        }


class ValueBase(BaseModel):
    project_id: int
    date: date
    plan_value: Optional[float]
    fact_value: Optional[float]

    class Config:
        json_schema_extra = {
            'title': 'ValueBase',
            'description': 'Example ValueBase message',
            'example': {
                'project_id': 1,
                'date': datetime.date(2022, 11, 24),
                'plan_value': 12.23,
                'fact_value': 14.4567
            }
        }


class Success(BaseModel):
    result: bool = True


class FileSuccess(Success):
    file_id: int
    body_message: str

    class Config:
        json_schema_extra = {
            'title': 'FileSuccess',
            'description': 'Example FileSuccess message',
            'example':
                {
                    'result': True,
                    'file_id': 12,
                    'body_message': 'Файл уcпешно обновлен!'
                }

        }


class Failure(Success):
    error_type: str
    body_message: str

    class Config:
        # пример того как должны выглядеть данные для документации
        json_schema_extra = {
            'title': 'Failure',
            'description': 'Example Failure message',
            'examples': [
                {
                    'result': True,
                    'error_type': 'Тип ошибки',
                    'body_message': 'Тект ошибки'
                },
            ]
        }


class ResponseModel(Success):
    content: bytes
    body_message: str
    filename: str  # Добавлено поле для имени файла
    content_type: str

    class Config:
        json_schema_extra = {
            "title": "ResponseModel",
            "description": "Example ResponseModel",
            'example': {
                'return': True,
                'content': 'content',
                'body_message': 'Файл успешно выгружен!',
                'filename': 'file.xlsx',
                'content_type': 'content_type'
            }
        }
