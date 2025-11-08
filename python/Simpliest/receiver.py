#https://timeweb.cloud/tutorials/microservices/ustanovka-i-nastroika-rabbitmq

from pika import BlockingConnection, SSLOptions, ConnectionParameters, PlainCredentials, URLParameters 
from pika.exchange_type import ExchangeType
import sys, os


hostname="amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com:5671/jmnvgeqr"


def receiver_run(host):
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









