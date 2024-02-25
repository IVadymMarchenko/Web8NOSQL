from mongoengine import Document,connect
from mongoengine.fields import ListField,StringField,BooleanField




class Contact(Document):
    fullname=StringField(required=True)
    email=StringField(required=True,unique=True)
    phone=StringField(required=True)
    is_mail_send=BooleanField(default=False)



