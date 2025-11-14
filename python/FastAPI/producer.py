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



app = FastAPI()


"""
@app.post("/send_message/")
async def send_message_async(txt):
    connection = await aio_pika.connect_robust(pika.URLParameters(hostname))
    channel = await connection.channel()
    #exch='fast_api'
    #exch_type='direct'
    #alt_exh = 'DLEX'
    channel.exchange_declare(exchange=exch,
                         exchange_type=exch_type,
                         durable=True,
                         arguments={'alternate-exchange': alt_exh})
    queue = await channel.declare_queue("fastapi_queue")
    message_body = json.dumps(email_body.dict())
    message = aio_pika.Message(body=message_body.encode(), content_type='application/json')
    await exchange.publish(message, routing_key="send_email")
    #return {"status": "Message sent to the queue"}
    print("message is sended: ", message)
"""
    

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

