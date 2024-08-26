from aiokafka import AIOKafkaProducer

aio_producer: AIOKafkaProducer | None = None


async def get_producer():
    return aio_producer
