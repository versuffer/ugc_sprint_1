from app.fastapi_app.schemas.services.metric_schemas import BaseMetricSchema


class KafkaProducer:
    def save_metric(self, metric: BaseMetricSchema):
        pass
