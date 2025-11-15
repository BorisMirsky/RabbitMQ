from fastapi import FastAPI
from pydantic import BaseModel
import aio_pika
import pika
from pika.exchange_type import ExchangeType
import json
from model import EmailBody
from hostname import hostname
import random
import string
import asyncio




async def send_txt(email_body):
    print(f"Sending email to {email_body['user_email']} with subject {email_body['subject']}")
    if "error" in email_body['subject'].lower():
        raise Exception("Failed to send email")


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        txt = json.loads(message.body)
        try:
            #await send_txt(email_body)
            await send_callback(txt, message.correlation_id)
        except Exception as e:
            await send_callback(txt, message.correlation_id, str(e))


async def send_callback(txt, correlation_id, exception=None):
    connection = await aio_pika.connect_robust(hostname)
    channel = await connection.channel()
    exchange = await channel.declare_exchange("fast_api_exchange", aio_pika.ExchangeType.DIRECT)
    callback_queue = await channel.declare_queue("fast_api_queue")
    if exception:
        result = {"status": "failed", "reason": exception}
    else:
        result = {"status": "success"}
    result_message = aio_pika.Message(body=json.dumps(result).encode(), content_type='application/json')
    await exchange.publish(result_message, routing_key="callback")


async def consume():
    connection = await aio_pika.connect_robust(hostname)
    channel = await connection.channel()
    queue = await channel.declare_queue("fast_api_queue")
    await queue.consume(process_message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
    loop.run_forever()



    
