from datetime import datetime
from typing import List

import requests
from loguru import logger

from config_bot import headers


@logger.catch
def hotels_info_for_bestdeal(town_id: str,
                             count_of_hotels: int,
                             min_price: int,
                             max_price: int,
                             min_distance: int,
                             max_distance: int,
                             in_date: str,
                             out_date: str) -> List[dict] or None:
    """
    Функция. Осуществляет запрос к API Hotels для получения списка отелей
    и их характеристик по-заданному ID города для команд bestdeal.
    :param town_id: id города, для запроса.
    :param count_of_hotels: количество отелей, которое запросил пользователь.
    :param min_price: минимальная цена проживания.
    :param max_price: максимальная цена проживания.
    :param min_distance: минимальная удаленность отеля от центра города.
    :param max_distance: максимальная удаленность отеля от центра города.
    :param in_date: дата заезда в отель.
    :param out_date: дата выезда из отеля.
    :return: список словарей из найденных отелей и их характеристик в формате:
        "ID": "цифровое значение ID города"
        "Наименование": "полное наименование отеля"
        "Адрес": "полный адрес отеля"
        "Рейтинг": "цифровое значение рейтинга отеля"
        "Расстояние": "расстояние от центра города до отеля"
        "Цена": "стоимость пребывания в отеле за сутки"
        "Цена за все время": "стоимость пребывания в отеле за весь период"
    """

    url_hotels = 'https://hotels4.p.rapidapi.com/properties/list'
    querystring = {"destinationId": town_id,
                   "pageNumber": "1",
                   "checkIn": in_date,
                   "checkOut": out_date,
                   "adults1": "1",
                   "priceMin": min_price,
                   "priceMax": max_price,
                   "sortOrder": "PRICE",
                   "locale": "ru_RU",
                   "currency": "RUB",
                   }

    try:
        response = requests.request("GET", url_hotels,
                                    headers=headers,
                                    params=querystring,
                                    timeout=30)

        if response.status_code != 200:
            return None

        founded_hotels = response.json()
        hotels_list = [{'id': hotel['id'],
                        'name': hotel['name'],
                        'address': hotel.get('address', {}).get('streetAddress'),
                        'rating': str(hotel['starRating']) + '*',
                        'distance': hotel['landmarks'][0]['distance'],
                        'cur_price': hotel['ratePlan']['price']['current'],
                        'overall_price': str(int(
                            (datetime.strptime(out_date, "%Y-%m-%d").date() -
                             datetime.strptime(in_date, "%Y-%m-%d").date()).days) *
                                         int(hotel['ratePlan']['price']['exactCurrent'])) + ' RUB'
                        }
                       for hotel in founded_hotels['data']['body']['searchResults']['results']]

        for dicts in hotels_list:
            for key, value in dicts.items():
                if value is None:
                    dicts[key] = 'Информация отсутствует'

        bestdeal_hotels_list = list(filter(lambda elem:
                                           max_distance >= string_to_float(elem['distance']) >= min_distance,
                                           hotels_list))

        return bestdeal_hotels_list[:count_of_hotels]
    except requests.exceptions.RequestException as e:
        logger.info(f'{e} exceptions on step "hotels_info_for_bestdeal"')
        return None


@logger.catch
def string_to_float(string: str) -> float:
    """
    Функция. Преобразует текстовое значение числа в вещественное значение.
    :param string: строка, содержащая текстовое значение вещественного числа.
    :return: вещественное значение числа
    """
    string_elements = string.split()
    number_elem = string_elements[0].split(',')
    if len(number_elem) != 1:
        float_number = float('.'.join(number_elem))
    else:
        float_number = float(number_elem[0])
    return float_number
