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

    def _get_parsed_metric(self, metric_schema: TransferMetricSchema) -> BaseMetricSchema | None:
        if parsing_schema := self.metric_mapping.get(metric_schema.metric_name):
            try:
                return parsing_schema(**metric_schema.get_dict())
            except ValidationError as error:
                logger.error(
                    f'Ошибка валидации метрики {metric_schema.metric_name}: {error}. '
                    f'Данные не сохранены: {metric_schema}.'
                )
                return None
        logger.error(
            f'Попытка сохранить неизвестный тип метрики: {metric_schema.metric_name}. '
            f'Данные не сохранены: {metric_schema}.'
        )
        return None

    async def send_metric(self, metric_info: MetricsSchemaIn, user_token: str, producer: AIOKafkaProducer) -> None:
        try:
            user_id = self.auth_service.get_user_id(user_token)
        except JWTError as error:
            logger.error(f'Ошибка идентификации пользователя: {error}. Данные не сохранены: {metric_info.metric_data}')
            return
        if metric := self._get_parsed_metric(
            TransferMetricSchema(
                user_id=user_id,
                metric_name=metric_info.metric_name,
                data=metric_info.metric_data,
            )
        ):
            await producer.send(
                topic=metric.metric_name,
                value=metric.model_dump_json().encode(),
                key=f'{user_id}'.encode(),
            )
            logger.info('Данные успешно отправлены в Кафку.')
