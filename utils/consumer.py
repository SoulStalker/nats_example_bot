import asyncio
from asyncio import CancelledError
from datetime import datetime, timedelta, timezone

import nats
from nats.aio.msg import Msg

from config_data.config import load_config

config = load_config()


# Функция-обработчик полученных сообщений
async def on_message(msg: Msg):
    # Получаем из заголовков сообщения время отправки и время задержки
    sent_time = datetime.fromtimestamp(float(msg.headers.get('Tg-Delayed-Msg-Timestamp')), tz=timezone.utc)
    delay = int(msg.headers.get('Tg-Delayed-Msg-Delay'))

    # Проверяем наступило ли время обработки сообщения
    if sent_time + timedelta(seconds=delay) > datetime.now().astimezone():
        # Если время обработки не наступило - вычисляем сколько секунд осталось до обработки
        new_delay = (sent_time + timedelta(seconds=delay) - datetime.now().astimezone()).total_seconds()
        # Отправляем nak с временем задержки
        await msg.nak(delay=new_delay)
    else:
        # Если время обработки наступило - выводим информацию в консоль
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received '{data}' from subject `{subject}`")
        await msg.ack()


async def main():
    # Подключаемся к NATS серверу
    nc = await nats.connect(servers=config.nats.servers)
    # Получаем JetStream контекст
    js = nc.jetstream()

    # Сабджект для подписки
    subject = 'aiogram.delayed.messages'
    # Стрим для подписки
    stream = 'aiogram_delayed'

    # Подписываемся на указанный стрим
    await js.subscribe(
        subject=subject,
        stream=stream,
        cb=on_message,
        durable='delayed_message_consumer',
        manual_ack=True
    )

    print(f"Subscribed to subject '{subject}'")

    # Создаем future для поддержания соединения открытым
    try:
        await asyncio.Future()
    except CancelledError:
        pass
    finally:
        # Закрываем соединение
        await nc.close()


asyncio.run(main())
