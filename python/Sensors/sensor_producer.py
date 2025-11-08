#https://babok-school.ru/blog/how-to-write-producer-and-consumer-for-rabbitmq-in-colab/

from pika import BlockingConnection, SSLOptions, ConnectionParameters, PlainCredentials, URLParameters 
from pika.exchange_type import ExchangeType
import json
import random
import time




# Connect to RabbitMQ server
hostname="amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com:5671/jmnvgeqr" 

connection = BlockingConnection(URLParameters(hostname))
channel = connection.channel()

# Declare an exchange
channel.exchange_declare(exchange='sensor_exchange_1', exchange_type='direct')

# Prepare a list of divices
devices =[random.randint(0, 100) for i in range(100)]

# Prepare a list of possible routing keys
routing_keys = ['pressure_1', 'temperature_1']

while True:
    # Prepare random message in JSON format
    measure=random.choice(routing_keys)
    data = {'device': random.choice(devices), 'measure': measure, 'value': random.randint(0,100)}
    message = json.dumps(data)

    # Send the message to the exchange
    channel.basic_publish(exchange='sensor_exchange_1', routing_key=measure, body=message)
    print(f' [x] Sent {message}')

    # Sleep for 3 seconds
    time.sleep(3)

channel.close()
connection.close()


