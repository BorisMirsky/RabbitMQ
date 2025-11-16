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


async def callback(message):
    txt = message.body.decode("utf-8")
    data = json.loads(txt)
    print('data from callback ', data)
    #await db["preds"].insert_one(data)


async def main(loop):
    connection = await aio_pika.connect(hostname, loop = loop)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)
    await queue.consume(callback, no_ack = True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()




    
