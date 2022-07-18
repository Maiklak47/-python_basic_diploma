# -*- coding: utf8 -*-
from api_request.city_id_request import search_city

from handlers.default_heandlers.start_help import cancel_request
from loader import bot
from telebot import types
from loguru import logger


@logger.catch
def city_choice_keyboard(message: types.Message) -> None:
    """
    Функция, которая создает клавиатуру для выбора города из списка найденных городов.
    :param message: сообщение пользователя с названием города.
    :return: None
    """
    if message.text == '/help':
        cancel_request(message)
        return
    logger.info(f'Make a list of cities for user {message.chat.id}')
    bot.send_message(chat_id=message.chat.id, text='Ведется поиск...')
    chat_id = message.chat.id
    city = message.text.title()
    city_list = search_city(city=city)

    if city_list is None:
        bot.send_message(chat_id=message.chat.id, text='Не удается получить информацию с сайта.'
                                                       'Повторите запрос позднее.')
        return

    markup = types.InlineKeyboardMarkup(row_width=5)
    for i in city_list:
        for city_id, region in i.items():
            button_value = region.split(',')[0]
            markup.add(types.InlineKeyboardButton(text=region,
                                                  callback_data=('|'.join([button_value,
                                                                           str(city_id),
                                                                           str(chat_id)]))))
    markup.add(types.InlineKeyboardButton(text='Отмена',
                                          callback_data='help'))

    if len(city_list) == 0:
        logger.info(f'City for user {message.chat.id} is not found')
        msg = bot.send_message(chat_id=chat_id, text=f'Город {city} не найден. Повторите ввод.')
        bot.register_next_step_handler(message=msg, callback=city_choice_keyboard)
    else:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        bot.send_message(chat_id=message.chat.id, text='Выберите город:', reply_markup=markup)
