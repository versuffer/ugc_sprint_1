import logging
from pprint import pformat

import uvicorn
from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

from app.fastapi_app.api.api_router import api_router
from app.fastapi_app.settings.config import settings
from app.fastapi_app.settings.logs import logger
from app.kafka.producers import kafka_producer

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION, version="1", debug=settings.DEBUG)


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():
    kafka_producer.aio_producer = AIOKafkaProducer(
        **{'bootstrap_servers': '{}:{}'.format(settings.KAFKA_HOST, settings.KAFKA_PORT)}
    )
    await kafka_producer.aio_producer.start()


@app.on_event("shutdown")
async def shutdown():
    await kafka_producer.aio_producer.stop()


if __name__ == "__main__":
    logger.info(f"Start server. Settings: \n{pformat(settings.dict())}")

    uvicorn.run("main:app", host="localhost", port=8000, log_level=logging.DEBUG)
