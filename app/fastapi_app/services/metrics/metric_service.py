import asyncio
import time

from app.fastapi_app.schemas.api.v1.schemas import MetricsSchemaIn
from app.fastapi_app.services.auth.auth_service import AuthService
from app.fastapi_app.services.repositories.kafka.producers import KafkaProducer
from app.fastapi_app.settings.logs import logger


class MetricService:
    def __init__(self):
        self.auth_service = AuthService()
        self.kafka_producer = KafkaProducer()

    def get_prepared_metric(self, raw_metric):
        pass

    def save_metric(self, data: MetricsSchemaIn):
        # time.sleep(5)
        if not self.auth_service.is_user_token_valid(data.user_token):
            logger.error(
                f'Пользователь с токеном {data.user_token} не найден. Данные не сохранены: {data.metric_data}'
            )
        if metric := self.get_prepared_metric(data.metric_data):
            self.kafka_producer.save_metric(metric)
            logger.info(f'Данные отправлены в сервис Кафки для сохранения {metric}.')
