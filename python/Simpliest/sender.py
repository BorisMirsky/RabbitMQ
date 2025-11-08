from pika import BlockingConnection, SSLOptions, ConnectionParameters, PlainCredentials, URLParameters 
from pika.exchange_type import ExchangeType
import random
#import os
#import socket
#import ssl


hostname="amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com:5671/jmnvgeqr" 

def sender_run(host):
    parameters = URLParameters(host)
    connection = BlockingConnection(parameters)
    # создаём канал
    channel = connection.channel()
    # создаём обменник
    channel.exchange_declare('new_exchange', ExchangeType.direct)
    # определяем очередь
    queue = channel.queue_declare(queue='new_queue')
    # привязываем очередь к обменнику
    channel.queue_bind(exchange='new_exchange', queue='new_queue', routing_key='key') 
    # публикуем сообщение
    number = random.randint(1, 1000)
    txt = "Hello World {}".format(number)
    channel.basic_publish(exchange='new_exchange', routing_key='key', body=txt)
    print("Сообщение {} отправлено".format(txt))
    connection.close()


sender_run(hostname)
