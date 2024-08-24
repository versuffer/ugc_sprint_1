from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from starlette import status

from app.fastapi_app.schemas.api.v1.schemas import MetricsSchemaIn
from app.fastapi_app.services.auth.auth_service import AuthService
from app.fastapi_app.services.kafka_producer import get_producer
from app.fastapi_app.services.metrics.metric_service import MetricService
from app.fastapi_app.settings.logs import logger

router = APIRouter()


@router.post("/metrics", status_code=status.HTTP_202_ACCEPTED)
async def save_metrics(
    data: MetricsSchemaIn,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(),
    producer: AIOKafkaProducer = Depends(get_producer),
):
    """
    Проверяет права доступа у внешнего сервиса.
    Авторизованным сервисам сразу возвращает ответ и в фоновой задаче сохраняет метрики.


    Пример запроса:

        {
          "service_name": "front",
          "user_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
          "metric_name": "click",
          "metric_data": {"element_id": "button33"}
        }


    """
    if not auth_service.is_service_authorized(data.service_name):
        logger.warning(f"Unknown service try to save metrics: {data.service_name}.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Сервис не авторизован.')
    background_tasks.add_task(MetricService().save_metric, data, producer)
