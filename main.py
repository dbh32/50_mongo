import csv
from pprint import pprint
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# hw = homework
hw_db = client['hw_db']
concerts_collection = hw_db.concerts


# cc = concerts_collection

def show_cc():
    for concert in concerts_collection.find():
        pprint(concert)


def drop_cc():
    hw_db.drop_collection(concerts_collection)


def read_data(csv_file):
    """
    Загрузить данные в бд из CSV-файла
    """
    with open(csv_file, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        concerts_list = []
        for row in reader:
            concert = {'name': row['Исполнитель'],
                       'price': int(row['Цена']),
                       'place': row['Место'],
                       'date': row['Дата']}
            concerts_list.append(concert)
        result = concerts_collection.insert_many(concerts_list)
    return result


def find_cheapest():
    """
    Отсортировать билеты из базы по возрастания цены
    Документация: https://docs.mongodb.com/manual/reference/method/cursor.sort/
    """
    for concert in concerts_collection.find().sort('price', 1):
        print(f'Билеты на "{concert["name"]}" стоят {concert["price"]} рублей')


def find_by_name(name):
    """
    Найти билеты по имени исполнителя (в том числе – по подстроке),
    и вернуть их по возрастанию цены
    """
    for concert in concerts_collection.find({'name': {'$regex': name}}).sort('price', 1):
        print(f'Билеты на {concert["name"]}, '
              f'{concert["date"]} в {concert["place"]} стоят {concert["price"]}')
    print()


if __name__ == '__main__':
    drop_cc()
    read_data('artists.csv')
    show_cc()
    find_cheapest()
    find_by_name('-')
