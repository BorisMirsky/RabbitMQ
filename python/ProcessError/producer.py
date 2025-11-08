
import pika
import json
import random
from datetime import datetime
import time
import os



# Подключение к серверу RabbitMQ server в облачной платформе cloudamqp.com
hostname="amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com:5671/jmnvgeqr" 

connection = pika.BlockingConnection(pika.URLParameters(hostname))
channel = connection.channel()

# объявление обменника
exch='REX'
exch_type='direct'
alt_exh = 'DLEX'
channel.exchange_declare(exchange=exch,
                         exchange_type=exch_type,
                         durable=True,
                         arguments={'alternate-exchange': alt_exh})

number=0 #начальный номер события

#бесконечный цикл публикации данных
while True:
  start_time = time.time()  # запоминаем время начала отправки сообщения
  #подготовка данных для публикации в JSON-формате
  producer_publish_time = time.strftime("%m/%d/%Y %H:%M:%S", time.localtime(start_time))

  number=number+1

  #задаем ключ маршрутизации (верный или для dlq)
  OK = random.choice([1,0])
  if OK==1:
    rk='rkey'
    content=f'ВСЕ НОРМАЛЬНО, произошло событие номер {number}'
    #создаем полезную нагрузку в JSON
    data = {'producer_publish_time': producer_publish_time,'content': content}
  else :
    rk=''
    content='НЕКОРРЕКТНОЕ измерение'
    data = {'event_time': producer_publish_time,'content': content}

  message = json.dumps(data)

  #отправка сообщения в обменник RabbitMQ с ключом маршрутизации и свойствами (заголовок)
  channel.basic_publish(exchange=exch, routing_key=rk, body=message)

  #вывод отладочной информации
  print(f' ключ маршрутизации {rk} Сообщение {number} отправлено {message}')

  #повтор через 3 секунды
  time.sleep(3)

#закрываем канал и соединение
channel.close()
connection.close()
