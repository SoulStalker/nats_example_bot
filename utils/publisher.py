import asyncio
from datetime import datetime
from config_data.config import load_config
import nats

config = load_config()


async def main():
    # Подключаемся к серверу NATS
    nc = await nats.connect(servers=config.nats.servers)

    # Желаемая задержка в секундах
    delay = 5

    message = 'Hello from python publisher!'

    # Заголовки
    headers = {
        'Tg-Delayed-Msg-Timestamp': str(datetime.now().timestamp()),
        'Tg-Delayed-Msg-Delay': str(delay)
    }

    # Сабджект, в который отправляется сообщение
    subject = 'aiogram.delayed.messages'

    # Публикуем сообщение на указанный сабджект
    await nc.publish(subject, message.encode('utf-8'), headers=headers)

    # Выводим в консоль информацию о том, что сообщение опубликовано
    print(f"Message '{message}' with headers {headers} published in subject '{subject}'")

    await nc.close()

asyncio.run(main())
