import logging

from aiogram import Bot
from services.dealy_service.consumer import DelayedMessageConsumer

from nats.aio.client import Client
from nats.js.client import JetStreamContext

loggger = logging.getLogger(__name__)


async def start_delayed_consumer(
    nc: Client,
    js: JetStreamContext,
    bot: Bot,
    subject: str,
    stream: str,
    durable_name: str
) -> None:
    consumer = DelayedMessageConsumer(
        nc=nc,
        js=js,
        subject=subject,
        stream=stream,
        durable_name=durable_name,
        bot=bot
    )
    loggger.info(f"Starting Delayed Message Consumer on {subject}")
    await consumer.start()
