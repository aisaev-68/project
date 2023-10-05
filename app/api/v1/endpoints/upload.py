from typing import Union, Annotated
from fastapi import APIRouter, UploadFile, File, status, Depends

from app.schema.schemas import Failure, FileSuccess
from app.crud.project import ProjectService
from app.utils.logger import get_logger

logger = get_logger("api.upload")

router = APIRouter()


@router.post(
    "",
    response_model=Union[FileSuccess, Failure],
    summary="Загружает файл",
    description="Маршрут - позволяет загрузить файл.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
async def upload_file(
        file: Annotated[bytes, File()],
        service: Annotated[ProjectService, Depends()]
) -> Union[FileSuccess, Failure]:

    try:
        file_id = await service.upload_data(file)

    except Exception as er:
        error_message = str(er)
        error_type = type(er).__name__
        logger.error(error_message)
        return Failure(result=False, error_type=error_type, body_message=error_message)

    return FileSuccess(result=True, file_id=file_id, body_message="Файл уcпешно обработан!")