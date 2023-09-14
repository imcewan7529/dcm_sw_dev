# receiver.py
# run this to watch all messages sent on the exchange
import pika

def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

def listen_for_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    exchange_name = 'DCM_Main_Exchange'
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    print('Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    listen_for_messages()