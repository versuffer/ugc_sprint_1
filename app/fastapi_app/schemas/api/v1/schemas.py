from pydantic import BaseModel


class MetricsSchemaIn(BaseModel):
    service_name: str
    user_token: str
    metric_name: str
    metric_data: dict
