import pika
import json

params = pika.URLParameters('your-rabbitmq-url')
connection = pika.BlockingConnection(params)
channel = connection.channel()


# def publish():
#     channel.basic_publish(exchange='', routing_key='main', body='hello')

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
