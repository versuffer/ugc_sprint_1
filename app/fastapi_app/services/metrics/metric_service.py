from aiokafka import AIOKafkaProducer
from pydantic import ValidationError

from app.fastapi_app.constants import METRIC_MAPPING
from app.fastapi_app.exeptions import JWTError
from app.fastapi_app.schemas.api.v1.schemas import MetricsSchemaIn
from app.fastapi_app.schemas.services.metric_schemas import (
    BaseMetricSchema,
    TransferMetricSchema,
)
from app.fastapi_app.services.auth.auth_service import AuthService
from app.fastapi_app.settings.logs import logger


class MetricService:
    def __init__(self):
        self.auth_service = AuthService()
        self.metric_mapping = METRIC_MAPPING

    def _get_prepared_metric(self, data: TransferMetricSchema) -> BaseMetricSchema | None:
        if schema := self.metric_mapping.get(data.metric_name):
            try:
                return schema(**data.get_dict())
            except ValidationError as error:
                logger.error(f'Ошибка валидации метрики {data.metric_name}: {error}. ' f'Данные не сохранены: {data}.')
                return None
        logger.warning(
            f'Попытка сохранить неизвестный тип метрики: {data.metric_name}. ' f'Данные не сохранены: {data}.'
        )
        return None

    async def save_metric(self, data: MetricsSchemaIn, producer: AIOKafkaProducer) -> None:
        if not self.auth_service.is_user_token_valid(data.user_token):
            logger.error(f'Пользователь с токеном {data.user_token} не найден. Данные не сохранены: {data.metric_data}')
            return
        try:
            user_id = self.auth_service.get_user_id(data.user_token)
        except JWTError as error:
            logger.error(f'Ошибка идентификации пользователя: {error}. Данные не сохранены: {data.metric_data}')
            return
        if metric := self._get_prepared_metric(
            TransferMetricSchema(
                user_id=user_id,
                metric_name=data.metric_name,
                data=data.metric_data,
            )
        ):
            await producer.send(
                topic=metric.metric_name,
                value=metric.json().encode(),
                key=f"{user_id}".encode(),
            )
            logger.info('Данные успешно отправлены в Кафку.')
