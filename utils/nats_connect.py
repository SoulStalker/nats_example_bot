import nats
from nats.aio.client import Client as NatsClient
from nats.js import JetStreamContext


async def connect_to_nats(servers: list[str]) -> tuple[NatsClient, JetStreamContext]:
    """
    Задача асинхронной функции connect_to_nats состоит в том,
    чтобы подключиться к серверу NATS и вернуть два объекта: клиент NATS и контекст JetStream,
    с которыми можно будет работать в дальнейшем
    :param servers:
    :return: nc, js
    """
    nc: NatsClient = await nats.connect(servers=servers)
    js: JetStreamContext = nc.jetstream()

    return nc, js
