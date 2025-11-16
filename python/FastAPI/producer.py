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


app = FastAPI()

# =====================   post async =====================
@app.post("/send_message_async")
async def send_message_async(txt):
    exch = 'fast_api_exchange'
    queue_name = 'fast_api_queue'
    connection = await aio_pika.connect_robust(hostname) 
    channel = await connection.channel()
    exchange = await channel.declare_exchange(exch, aio_pika.ExchangeType.DIRECT)
    queue = await channel.declare_queue(queue_name)
    message_body = json.dumps(txt)
    message = aio_pika.Message(body=message_body.encode(), content_type='application/json')
    await exchange.publish(message, routing_key="key")
    connection.close()



# ========================== post =============================
@app.post("/send_message")
def send_message(txt):   
    parameters = pika.URLParameters(hostname)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    exch = 'fast_api_exchange'
    queue_name = 'fast_api_queue'
    channel.exchange_declare(exch, ExchangeType.direct)
    queue = channel.queue_declare(queue=queue_name)
    channel.queue_bind(exchange=exch, queue=queue_name, routing_key='key')
    channel.basic_publish(exchange=exch, routing_key='key', body=txt)
    print("Сообщение {} отправлено".format(txt))
    connection.close()


message = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
send_message(message)

message_async = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + '_async'
#loop = asyncio.get_event_loop()
#loop.run_until_complete(send_message_async(message_async))
#loop.run_forever()





