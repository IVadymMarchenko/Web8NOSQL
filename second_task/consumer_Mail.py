import pika
from models import Contact
from mongoengine import connect
from producer import URI

connect(db='test',host=URI)
def send_mail(contact):#заглушка
    print(f'Send mail to {contact.id}')


def callback(ch,method,properties,body):
    contact_id=body.decode()
    contact=Contact.objects.get(id=contact_id)
    send_mail(contact)
    contact.is_mail_send=True
    contact.save()
    print(f'Mail sent to {contact.id}')


def main():
    credentials = pika.PlainCredentials('admin', '12345')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/',
                                                                   credentials=credentials))  # параметры подключения

    channel = connection.channel()  # создаем канал
    channel.queue_declare(queue='Mail') #создаем очередь
    channel.basic_consume(queue='Mail', on_message_callback=callback, auto_ack=True)
    print(f'[*] Waiting for message')
    channel.start_consuming()

if __name__ == '__main__':
    main()

