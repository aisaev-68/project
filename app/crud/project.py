from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, func
from sqlalchemy.orm import selectinload

from app.config import settings
from app.models.database import get_db
from app.models.models import Project, FileVersion, Value
from app.utils.logger import get_logger
from app.utils.handler_excel import process_excel_data

logger = get_logger("crud.project")


class ProjectService:
    """Класс для обработки Endpoint связанных с файлами."""

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def upload_data(
            self,
            file: bytes,
    ):
        """
        Метод для записи полученного файла.

        :param file: Полученный файл
        :return: идентификатор файла в базе.
        """

        add_file = FileVersion()
        self.session.add(add_file)
        await self.session.commit()

        data = await process_excel_data(file)  # тут проработать

        for project in data:
            item_project = Project(
                code=project['code'],
                name=project['project'],
                file_version_id=add_file.id
            )
            self.session.add(item_project)
            await self.session.flush()

            for plan_fact in project['values']:
                value = Value(
                    project_id=item_project.id,
                    date=plan_fact['date'],
                    plan_value=plan_fact['plan_value'],
                    fact_value=plan_fact['fact_value']
                )
                self.session.add(value)
        await self.session.commit()
        logger.info("Данные полученного файла записаны в базу")
        return add_file.id

    async def get_data_from_db(self, version_id) -> List:
        """
        Функция для получения данных из базы по версии файла.
        :param version_id: версия файла.
        :return: список данных.
        """

        projects = (await self.session.execute(
            select(Project).filter(Project.file_version_id == version_id).options(selectinload(Project.values))))

        data_from_db = [await project[0].to_json() for project in projects.all()]

        if not data_from_db:
            raise HTTPException(status_code=404, detail="Такая версия файла в базе нет.")
        logger.info("Данные из базы соответствующие версии файла извлечены")
        return data_from_db

    async def get_chart_data(self, version_id: int, year: int, value_type: str) -> List:
        """
        Функция для подготовки данных для диаграммы.
        :param version_id: версия файла.
        :param year: год.
        :param value_type: тип показателя.
        :return: список.
        """
        if value_type == settings.INDICATOR_FACT:
            stmt = (
                select(
                    Project.name,
                    Project.file_version_id,
                    extract('year', Value.date).label('year'),
                    func.sum(Value.fact_value).label('total_fact_value'))
                .join(Value)
                .filter(Project.file_version_id == version_id)
                .filter(extract('year', Value.date) == year)
                .group_by(Project.name, 'year', Project.file_version_id)
            )
        else:
            stmt = (
                select(
                    Project.name,
                    Project.file_version_id,
                    extract('year', Value.date).label('year'),
                    func.sum(Value.plan_value).label('total_plan_value'))
                .join(Value)
                .filter(Project.file_version_id == version_id)
                .filter(extract('year', Value.date) == year)
                .group_by(Project.name, 'year', Project.file_version_id)
            )

        result = await self.session.execute(stmt)

        if not result:
            raise HTTPException(status_code=404, detail="Данных нет.")

        chat_data = []

        # ('Проект 1', 1, Decimal('2022'), 6.540000000000001)
        for chunk in result:
            data = {}
            data['name'] = chunk[0]
            data['version_id'] = chunk[1]
            data['year'] = chunk[2]
            if chunk[3] and value_type == settings.INDICATOR_FACT:
                data['fact_value'] = chunk[3]
            else:
                data['plan_value'] = chunk[3]
            chat_data.append(data)
        logger.info("Данные для диаграммы сформированы")
        return chat_data
