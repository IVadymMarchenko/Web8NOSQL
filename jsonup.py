import json
from mongoengine import EmbeddedDocument, Document, connect
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField,ReferenceField
URI="mongodb+srv://topim31:Mbfeh6R2VkZy8ITL@cluster0.064gppv.mongodb.net/?retryWrites=true&w=majority"
connect(db='test',host=URI)

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    author = ReferenceField(Author)
    quote = StringField(required=True)
    tags = ListField(StringField())


def load_authors():
    with open("authors.json", 'r', encoding="utf-8") as file:
        data_of_authors = json.load(file)
        for author in data_of_authors:
            aut = Author(fullname=author.get("fullname"),
                         born_date=author.get("born_date"),
                         born_location=author.get("born_location"),
                         description=author.get("description"))
            aut.save()
def load_quotes():
    with open("qoutes.json", "r", encoding="utf-8") as file:
        data_quotes = json.load(file)
        for quote_data in data_quotes:
            author_name = quote_data.get('author')
            author = Author.objects.get(fullname=author_name) if author_name else None
            if author:
                quote = Quote(author=author,
                              tags=quote_data.get("tags"),
                              quote=quote_data.get("quote")
                             )
                quote.save()
            else:
                print(f"Author '{author_name}' not found.")




# quote = Quote.objects.first()  # Получение первой цитаты (это просто пример, вы можете использовать другие методы для получения цитат)
# if quote:
#     author_id = quote.author.id  # Получение идентификатора автора цитаты
#     author = Author.objects.get(id=author_id)  # Получение объекта автора по его идентификатору
#     print(author.fullname)  # Печать информации об авторе
# else:
#     print("No quotes found")




