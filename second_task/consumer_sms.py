import pika
from models import Contact
from mongoengine import connect
from producer import URI
connect(db='test',host=URI)

def send_sms(contact):
    print(f'Messeage was sent to {contact}')

def callback(ch,method,properties,body):
    contact_phone=body.decode()
    contact=Contact.objects.get(phone=contact_phone)
    send_sms(contact.phone)
    contact.save()
    print(f'SMS was sent to {contact.phone}')


def main():
    credentials = pika.PlainCredentials('admin', '12345')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/',
                                                                   credentials=credentials))  # параметры подключения

    channel = connection.channel()  # создаем канал
    channel.queue_declare(queue='SMS') #создаем очередь
    channel.basic_consume(queue='SMS', on_message_callback=callback, auto_ack=True)
    print(f'[*] Waiting for message')
    channel.start_consuming()

if __name__ == '__main__':
    main()
