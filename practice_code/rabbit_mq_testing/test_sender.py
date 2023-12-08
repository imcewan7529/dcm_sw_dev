# sender.py
# Run this to send messages on the exchange
import pika

def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    exchange_name = 'DCM_Main_Exchange'
    channel.basic_publish(exchange=exchange_name, routing_key='', body=message)
    connection.close()

if __name__ == '__main__':
    while True:
        message = input('Enter your message (or type "exit" to quit): ')
        if message.lower() == "exit":
            break
        send_message(message)
