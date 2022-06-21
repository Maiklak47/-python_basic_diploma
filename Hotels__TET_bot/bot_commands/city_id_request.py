import requests
import re

from loguru import logger
from typing import Optional, List

from config_bot import headers


@logger.catch
def search_city(city: Optional[str]) -> List[dict] or None:
    """
    Функция. Осуществляет запрос к API Hotels для получения списка городов,
    подходящих под заданное название.
    :param city: название города для запроса, которое указал пользователь.
    :return: список словарей из найденных городов в формате "ID города": "полное наименование города".
    """

    url_location = 'https://hotels4.p.rapidapi.com/locations/search'
    querystring = {'query': city, 'locale': "ru_RU"}

    if re.match(r'^[A-Za-z]', city):
        querystring['locale'] = 'en_US'
    try:
        response = requests.request('GET',
                                    url_location,
                                    headers=headers,
                                    params=querystring,
                                    timeout=30)
        if response.status_code != 200:
            return None

        founded_cities = response.json()
        city_list = []

        for i in founded_cities['suggestions'][0]['entities']:
            if i['name'].title() == city.title():
                caption = re.sub(r"^<span class='highlighted'>|</span>", '', i['caption']).split(',')[:2]
                city_list.append({i['destinationId']: ','.join(caption)})
        return city_list
    except requests.exceptions.RequestException as e:
        logger.info(f'{e} exceptions on step "search_city"')
        return None
