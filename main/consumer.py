import pika
import json
import django
from sys import path
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
settings_file = str(BASE_DIR / 'main/settings.py')
path.append(settings_file)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()

from shop.models import Product

params = pika.URLParameters('your-rabbitmq-url')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main', ch, method, properties, body)
    data = json.loads(body)
    print(data)
    if properties.content_type == "product_created":
        Product.objects.create(
            id=data['id'],
            title=data['title'],
            image=data['image'],
        )
    elif properties.content_type == "product_updated":
        product = Product.object.get(pk=data['id'])
        product.title = data['title']
        product.image = data['image']
        product.save()
    elif properties.content_type == "product_deleted":
        product = Product.object.get(pk=data)
        product.delete()


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
print('Started consuming')
channel.start_consuming()
channel.close()
