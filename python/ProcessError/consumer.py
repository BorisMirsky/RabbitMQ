
import pika
import json
import random
import requests
from datetime import datetime
from hostname import hostname

# Подключение к серверу RabbitMQ server в облачной платформе cloudamqp.com
connection = pika.BlockingConnection(pika.URLParameters(hostname))
channel = connection.channel()

#объявление очереди RQM
dlrk='dlkey'
alt_exh = 'DLEX'

my_queue='right_queue'
questions_queue = channel.queue_declare(queue=my_queue,
                                        arguments={'x-dead-letter-exchange': alt_exh,
                                                   'x-dead-letter-routing-key': dlrk}
                                        )

channel.queue_bind(exchange='REX',
                   queue=my_queue,
                   routing_key='rkey')

#начальный номер строки для записи данных
x=1

def on_inputs_message(channel, method, properties, body):
    global x

    try:
        # распаковка сообщения
        data = json.loads(body)

        # парсинг сообщения
        producer_publish_time = data['producer_publish_time']
        content = data['content']

        now = datetime.now()
        consuming_time = now.strftime("%m/%d/%Y %H:%M:%S")

        # вывод распарсенных данных в консоль
        print(f'{json.dumps(data)}')

        # обновление данных в Google Sheets
        print(x)
        x += 1
        with open("right_key.txt", "a") as f:
            f.write(x, producer_publish_time, consuming_time, content, sep=",   ")

    except Exception as e:
        # запись ошибок в лог-файл на Google Диске
        error_str = f"Error: {str(e)}, Value: {data}\n"
        with open("wrong_key.txt", "a") as f:
            f.write(error_str)
        print(f"Error: {str(e)}")

#потребляем данные из RabbitMQ
while True:
  print('Waiting for messages. To exit press CTRL+C')
  #привязка к очереди headers-обменника RQM
  channel.basic_consume(queue=questions_queue.method.queue,
                        on_message_callback=on_inputs_message,
                        auto_ack=True)
  channel.start_consuming()

#закрываем канал и соединение
channel.close()
connection.close()


