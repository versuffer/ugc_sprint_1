from fastapi import APIRouter, HTTPException
from starlette import status

from app.fastapi_app.settings.logs import logger

router = APIRouter()


@router.post("/metrics", status_code=status.HTTP_200_OK)
def save_metrics(
):
    logger.info(f"Post save_metrics.")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Unknown error')