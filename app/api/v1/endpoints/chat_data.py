from typing import Union, Annotated
from fastapi import APIRouter, status, Depends, Query

from app.crud.project import ProjectService
from app.schema.schemas import Failure, DataListPlan, DataListFact
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("api.chat_data")


router = APIRouter()


@router.get(
    "",
    response_model=Union[DataListPlan, DataListFact, Failure],
    summary="Формирует диаграмму",
    description="Маршрут - позволяет формировать диаграмму.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
async def chart_data(
        version_id: int,
        year: int,
        service: Annotated[ProjectService, Depends()],
        value_type: str = Query(..., title="Тип показателя (план или факт)")
) -> Union[DataListPlan, DataListFact, Failure]:
    try:
        chart_data = await service.get_chart_data(version_id, year, value_type)
        logger.info("Данные для диаграммы сформированы")
    except Exception as er:
        error_message = str(er)
        error_type = type(er).__name__
        logger.error(error_message)
        return Failure(result=False, error_type=error_type, body_message=error_message)
    if value_type == settings.INDICATOR_FACT:
        return DataListFact(projects=chart_data)
    else:
        return DataListPlan(projects=chart_data)
