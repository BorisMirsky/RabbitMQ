
from pika import BlockingConnection, SSLOptions, ConnectionParameters, PlainCredentials, URLParameters 
from pika.exchange_type import ExchangeType
import sys, os
from hostname import hostname



def receiver_run(host):
    parameters = URLParameters(host)
    connection = BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare('new_exchange', ExchangeType.direct)
    queue = channel.queue_declare(queue='new_queue')
    channel.queue_bind(exchange='new_exchange', queue='new_queue', routing_key='key')
    # функция, которая вызывается при получении сообщения
    def handle(channel, method, properties, body):
        print(f"Получено сообщение: {body.decode()}")
    # привязываем callback-функцию и очередь
    channel.basic_consume(queue='new_queue',
                          on_message_callback=handle,
                          auto_ack=True)
    print('Ожидание сообщения. Чтобы завершить работу приложения, нажмите ctrl+c')
    channel.start_consuming()

receiver_run(hostname)









