from pydantic import BaseModel


class MetricsSchemaIn(BaseModel):
    service_name: str
    metric_name: str
    metric_data: dict
