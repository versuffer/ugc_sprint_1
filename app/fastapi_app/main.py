import logging
from contextlib import asynccontextmanager
from pprint import pformat

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from app.fastapi_app.api.api_router import api_router
from app.fastapi_app.settings.config import settings
from app.fastapi_app.settings.logs import logger
from app.kafka.producers import kafka_producer


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        kafka_producer.aio_producer = AIOKafkaProducer(
            **{'bootstrap_servers': '{}:{}'.format(settings.KAFKA_HOST, settings.KAFKA_PORT)}
        )
        await kafka_producer.aio_producer.start()  # type: ignore
        yield
    finally:
        await kafka_producer.aio_producer.stop()  # type: ignore
        logger.info('Application stopped.')


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version="1.0.0",
    debug=settings.DEBUG,
    docs_url='/',
    lifespan=lifespan,
)
app.include_router(api_router)


if __name__ == "__main__":
    logger.info(f"Start server. Settings: \n{pformat(settings.dict())}")
    uvicorn.run("main:app", host="localhost", port=8000, log_level=logging.DEBUG)
