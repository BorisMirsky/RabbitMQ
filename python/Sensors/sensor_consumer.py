# https://babok-school.ru/blog/how-to-write-producer-and-consumer-for-rabbitmq-in-colab/

from pika import BlockingConnection, SSLOptions, ConnectionParameters, PlainCredentials, URLParameters 
from pika.exchange_type import ExchangeType
import json
import random
import time
from time import sleep



# Connect to RabbitMQ server
hostname="amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com:5671/jmnvgeqr" 

connection = BlockingConnection(URLParameters(hostname))
channel = connection.channel()

# Declare an exchange
channel.exchange_declare(exchange='sensor_exchange_1', exchange_type='direct')

temperature_queue = channel.queue_declare(queue='temperature_1')
pressure_queue = channel.queue_declare(queue='pressure_1')

channel.queue_bind(exchange='sensor_exchange_1',
                   queue=temperature_queue.method.queue,
                   routing_key='temperature_1')
channel.queue_bind(exchange='sensor_exchange_1',
                   queue=pressure_queue.method.queue,
                   routing_key='pressure_1')

def on_temperature_message(channel, method, properties, body):
   print("Температура ", json.loads(body))
   dictDataTemperature = json.loads(body)
   temperature_state = 'состояние температуры'
   temperature_value=int(dictDataTemperature['value'])
   if ((temperature_value) <= 80) and ((temperature_value) >= 20) :
     temperature_state = 'OK'
   else:
     temperature_state = 'ERROR'
   print("Устройство № ",
         dictDataTemperature["device"],
         "состояние температуры",
         temperature_state, "значение ",
         temperature_value)

   
def on_pressure_message(channel, method, properties, body):
   print("Pressure: ", json.loads(body))
   dictDataPressure = json.loads(body)
   pressure_state = 'состояние давления'
   pressure_value=int(dictDataPressure['value'])
   if ((pressure_value) <= 50) and ((pressure_value) >= 10) :
     pressure_state = 'OK'
   else:
     pressure_state = 'ERROR'
   print("Устройство № ",
         dictDataPressure["device"],
         "состояние давления",
         pressure_state,
         "значение ",
         pressure_value)


print('Waiting for messages. To exit press CTRL+C')


channel.basic_consume(queue=temperature_queue.method.queue,
                      on_message_callback=on_temperature_message,
                      auto_ack=True)
channel.basic_consume(queue=pressure_queue.method.queue,
                      on_message_callback=on_pressure_message,
                      auto_ack=True)
channel.start_consuming()


channel.close()
connection.close()


