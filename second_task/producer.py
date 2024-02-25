import pika
from faker import Faker
from models import Contact
from mongoengine import connect
import json

URI = "mongodb+srv://topim31:Mbfeh6R2VkZy8ITL@cluster0.064gppv.mongodb.net/?retryWrites=true&w=majority"
fake = Faker('uk_UA')

exchange_name=''
queue_name='Mail'
connect(db='test', host=URI)

def creat_task():
    for i in range(10):
        contact=Contact(fullname=fake.name(),email=fake.email(),phone=fake.phone_number())
        contact.save()

def main():

    credentials = pika.PlainCredentials('admin', '12345')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/',
                                                               credentials=credentials))  # параметры подключени
    channel = connection.channel()  # создаем канал
    channel.queue_declare(queue=queue_name)  # создаем очередь для маил

    channel.queue_declare(queue='SMS')#створюемо чергу СМС
    channel.exchange_declare(exchange='Send_SMS',exchange_type='direct')
    channel.queue_bind(exchange='Send_SMS', queue='SMS')

    for contact in Contact.objects:
        message=str(contact.id)
        phone=contact.phone.encode()
        channel.basic_publish(exchange=exchange_name, routing_key=queue_name,
                              body=message)  # Send message to consumer
        print(f'Send {contact.id} to rabbitMQ')
        channel.basic_publish(exchange='Send_SMS', routing_key='SMS', body=phone)
        print(f'Send {contact.phone} to rabbitMQ')
    channel.close()





if __name__ == '__main__':
    creat_task()#создаем контакты
    main()

