from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from starlette import status

from app.fastapi_app.schemas.api.v1.schemas import MetricsSchemaIn
from app.fastapi_app.services.auth.auth_service import AuthService, get_bearer_token
from app.fastapi_app.services.metrics.metric_service import MetricService
from app.fastapi_app.settings.logs import logger
from app.kafka.producers.kafka_producer import get_producer

metrics_router = APIRouter()


@metrics_router.post("/metrics", status_code=status.HTTP_202_ACCEPTED)
async def save_metrics(
    metric_info: MetricsSchemaIn,
    background_tasks: BackgroundTasks,
    access_token: str = Depends(get_bearer_token),
    auth_service: AuthService = Depends(),
    producer: AIOKafkaProducer = Depends(get_producer),
):
    """
    Проверяет права доступа у внешнего сервиса.
    Авторизованным сервисам сразу возвращает ответ и в фоновой задаче сохраняет метрики.

    Пример запроса:

        {
          "service_name": "front",
          "user_token": "eyJhbGciOiJIU...6yJV_adQssw5c",
          "metric_name": "click",
          "metric_data": {"element_id": "button33"}
        }


    """
    await auth_service.verify_user_token(token=access_token)
    if not auth_service.is_service_authorized(metric_info.service_name):
        logger.warning(f"Unknown service try to save metrics: {metric_info.service_name}.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Сервис не авторизован.')
    background_tasks.add_task(MetricService().send_metric, metric_info, access_token, producer)
