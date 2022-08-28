# -*- coding: utf8 -*-
import telebot
from telebot.types import InlineKeyboardMarkup


from telebot import types
from loguru import logger


@logger.catch
def city_choice_keyboard(city_list: dict) -> InlineKeyboardMarkup | None:
    """
    Функция, которая создает клавиатуру для выбора города из списка найденных городов.
    :param city_list: Список городов.
    :return: Inline клавиатуру.
    """
    city_name = InlineKeyboardMarkup()
    if city_list:
        for city in city_list:
            city_name.add(types.InlineKeyboardButton(text=city['city_name'],
                                                     callback_data=city['destination_id']))
        city_name.add(types.InlineKeyboardButton(text='Отмена',
                                                 callback_data='help'))
        logger.info(f'A keyboard has been created to select a city.')
        return city_name
    else:
        return None


@logger.catch
def yes_or_no():
    """Клавиатура для выбора фотографий 'да' или 'нет '
    """
    logger.info(f'The decision to choose a photo.')
    markup = types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Да', callback_data='Yes'))
    markup.add(telebot.types.InlineKeyboardButton(text='Нет', callback_data='No'))
    return markup
