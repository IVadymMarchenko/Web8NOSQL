from mongoengine import connect
from jsonup import Author, Quote
import redis
from jsonup import URI
from jsonup import load_authors,load_quotes


connect(db='test', host=URI)
redis_client = redis.Redis(host="localhost", port=6379, password=None, decode_responses=True)




def get_name_author(name_author):
    cached_data = redis_client.get(f'{name_author.encode()}')
    author = Author.objects(fullname__iregex=f'^{name_author}').first()
    if cached_data:
        print(author.fullname,cached_data,'cash')
    else:
        author = Author.objects(fullname__iregex=f'^{name_author}').first()
        if author:
            quotes = Quote.objects(author=author)
            quotes_text = '\n'.join(quote.quote for quote in quotes)
            key = f'{name_author}'
            redis_client.set(key, quotes_text)
            redis_client.expire(key, 30)  # Устанавливаем время жизни в секундах (здесь 1 час)
            print(author.fullname, quotes_text)
        else:
            print(f'Author with name "{name_author}" not found.')

def get_tag_author(name_tag):
    cached_data = redis_client.get(f'{name_tag.encode()}')
    if cached_data:
        print(cached_data,'cash')
    else:
        quotes = Quote.objects(tags__iregex=f'^{name_tag}')
        quotes_text = '\n'.join(quote.quote for quote in quotes)
        key = f'{name_tag}'
        redis_client.set(key, quotes_text)
        redis_client.expire(key, 30)  # Устанавливаем время жизни в секундах (здесь 1 час)
        print(quotes_text)


def get_tags_author(name_tags):
    value = name_tags.split(',')
    quotes = Quote.objects(tags=value[0])
    quotes1 = Quote.objects(tags=value[1])
    text=' '.join(str(i.quote) for i in quotes)
    text1 = ' '.join(str(i.quote) for i in quotes1)
    print(text)
    print(text1)


def main():

    while True:
        command=input('Enter command and value (format->command:value): ')
        cmd, value = command.split(':', 1)
        if cmd=='name':
            get_name_author(value)
        elif cmd==('tag'):
            get_tag_author(value)
        elif cmd==('tags'):
            get_tags_author(value)
        else:
            print('command is wrong')

if __name__ == '__main__':
    # load_authors()  #создаст авторов в базе
    # load_quotes() # добавит цытаты,теги
    main()


# quote = Quote.objects.first()  # Получение первой цитаты (это просто пример, вы можете использовать другие методы для получения цитат)
# if quote:
#     author_id = quote.author.id  # Получение идентификатора автора цитаты
#     author = Author.objects.get(id=author_id)  # Получение объекта автора по его идентификатору
#     print(author.fullname)  # Печать информации об авторе
# else:
#     print("No quotes found")





