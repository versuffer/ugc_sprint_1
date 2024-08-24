from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from starlette import status

from app.fastapi_app.schemas.api.v1.schemas import MetricsSchemaIn
from app.fastapi_app.services.auth.auth_service import AuthService
from app.fastapi_app.services.metrics.metric_service import MetricService
from app.fastapi_app.settings.logs import logger

router = APIRouter()


@router.post("/metrics", status_code=status.HTTP_202_ACCEPTED)
def save_metrics(
    data: MetricsSchemaIn,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends()
):
    """
    Проверяет права доступа у внешнего сервиса.
    Авторизованным сервисам сразу возвращает ответ и в фоновой задаче сохраняет метрики.
    """
    logger.info(f"Post save_metrics {data}.")
    if not auth_service.is_service_authorized(data.service_name):
        logger.warning(f"Unknown service try to save metrics: {data.service_name}.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Сервис не авторизован.')
    background_tasks.add_task(MetricService().save_metric, data)

