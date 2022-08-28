import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные не загружены, т.к. отсутствует файл .env")
else:
    load_dotenv()

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': os.getenv('RAPID_API_KEY')
}
URL_HOST = 'https://hotels4.p.rapidapi.com/'
URL_PATHS = {
    'locations': 'locations/v2/search',
    'properties': 'properties/list',
    'photos': 'properties/get-hotel-photos'
}
BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку/Отменить команду"),
    ('lowprice', "Поиск отелей с низкой ценой"),
    ('highprice', "Поиск отелей с самой высокой ценой"),
    ('bestdeal', "Поиск отелей подходящих по цене и расположению от центра"),
    ('history', "Вывод истории поиска отелей"),
)
