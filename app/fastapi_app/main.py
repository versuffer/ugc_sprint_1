import logging
from pprint import pformat

import uvicorn
from fastapi import FastAPI

from app.fastapi_app.api.api_router import api_router
from app.fastapi_app.settings.config import settings
from app.fastapi_app.settings.logs import logger

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION, version="1", debug=settings.DEBUG)


app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    logger.info(f"Start server. Settings: \n{pformat(settings.dict())}")

    uvicorn.run("main:app", host="localhost", port=8000, log_level=logging.DEBUG)
