from app.fastapi_app.schemas.services.metric_schemas import (
    ClickSchema,
    PageViewSchema,
    SearchFiltersSchema,
    VideoQualitySchema,
    VideoViewToTheEndSchema,
)

DEFAULT_ERROR_MESSAGE = 'Неизвестная ошибка.'

METRIC_MAPPING = {
    'click': ClickSchema,
    'page_view': PageViewSchema,
    'video_quality_change': VideoQualitySchema,
    'video_view_to_the_end': VideoViewToTheEndSchema,
    'search_filters': SearchFiltersSchema,
}
