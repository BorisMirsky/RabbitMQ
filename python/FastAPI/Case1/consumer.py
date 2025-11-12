import pika, sys, os


def receiver():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='logs')

    def callback(ch, method, properties, body:dict):
        print(" [x] Received %r" % body)
        log = f"This is the body : {body}"

    channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)


    print(' [*] Waiting for messages.')
    channel.start_consuming()

import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='logs')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
