import base64
from typing import Union, Annotated
from fastapi import APIRouter, status, Depends

from app.schema.schemas import Failure, ResponseModel
from app.crud.project import ProjectService
from app.utils.handler_excel import write_to_excel
from app.utils.logger import get_logger

logger = get_logger("api.export")

router = APIRouter()


@router.get(
    "/{version_id}",
    response_model=Union[ResponseModel, Failure],
    summary="Экспортирует файл",
    description="Маршрут - позволяет экспортировать файл.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
async def export_file(
        version_id: int,
        service: Annotated[ProjectService, Depends()]
) -> Union[ResponseModel, Failure]:
    try:
        data = await service.get_data_from_db(version_id)
        if not data:
            logger.info(f'Данные о версии файла {version_id} отсутствуют в базе')
            return Failure(result=False, error_type='',
                           body_message=f'Данные о версии файла {version_id} отсутствуют в базе')

        logger.info(f'Данные для скачивания файла сформированы')
        bytes_excel_file = write_to_excel(data)
        return ResponseModel(result=True, content=base64.b64encode(bytes_excel_file).decode('utf-8'),
                             body_message='Файл доставлен!', filename='file.xlsx',
                             content_type='application/octet-stream')
    except Exception as er:
        logger.info(f'Данные для скачивания файла сформированы')
        error_message = str(er)
        error_type = type(er).__name__
        logger.error(error_message)
        return Failure(result=False, error_type=error_type, body_message=error_message)
