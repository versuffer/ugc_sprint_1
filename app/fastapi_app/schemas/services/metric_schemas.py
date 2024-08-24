from pydantic import BaseModel


class BaseMetricSchema(BaseModel):
    user_id: str
    metric_name: str


class TransferMetricSchema(BaseMetricSchema):
    data: dict

    def get_dict(self) -> dict:
        result = {key: value for key, value in self.__dict__.items() if key != 'data'}
        result.update(self.data)
        return result


class ClickSchema(BaseMetricSchema):
    element_id: str


class PageViewSchema(BaseMetricSchema):
    url: str


class VideoQualitySchema(BaseMetricSchema):
    video_id: str
    prev_quality: str
    new_quality: str


class VideoViewToTheEndSchema(BaseMetricSchema):
    video_id: str


class SearchFiltersSchema(BaseMetricSchema):
    filter_name: str
