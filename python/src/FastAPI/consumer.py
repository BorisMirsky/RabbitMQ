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


queue_name = 'fast_api_queue'

async def main():
    connection = await aio_pika.connect_robust(hostname,)

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)
        #await channel.default_exchange.publish(aio_pika.Message(body="Hello, world!".encode()),routing_key="my_queue",)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(f"Received message: {message.body.decode()}")
                    break 


asyncio.run(main())




    
