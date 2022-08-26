# -*- coding: utf8 -*-

from handlers.default_heandlers.start_help import help_message, cancel_request

from loader import bot
from utils.kalendar import get_check_in_out_date
from utils.results import result
from loguru import logger
from telebot import types
from database.chat_users_db import set_info, get_info
from states.user_states import UserState


@logger.catch
@bot.message_handler(content_types=['text'])
def message_check(message: types.Message) -> None:
    """
    Функция. Отлавливает некорректные команды.
    :param message: любое сообщение от пользователя, не являющееся командой.
    :return: None
    """
    logger.info(f'User {message.chat.id} input unknown command.')
    bot.send_message(chat_id=message.chat.id, text='Введена неизвестная команда.')
    help_message(message)


@logger.catch
def get_hotels_count(message: types.Message) -> None:
    """
    Функция, которая создает клавиатуру для уточнения необходимости выгрузки фотографий.
    Принимает от пользователя количество отелей для выгрузки.
    :param message: сообщение пользователя с количеством отелей.
    :return: None
    """
    if message.text == '/help':
        cancel_request(message)
        return

    if message.text.isdigit():
        if not 25 >= int(message.text) > 0:
            logger.info(f'User {message.chat.id} chose wrong number of hotels.')
            msg = bot.send_message(chat_id=message.chat.id, text='Указано некорректное значение.\n'
                                                                 'Укажите от 1 до 25 отелей.')
            bot.register_next_step_handler(message=msg, callback=get_hotels_count)
            return

        else:
            logger.info(f'Ask user {message.chat.id} about hotel photo.')
            chat_id = message.chat.id
            set_info(column='hotels_count', value=message.text, user_id=chat_id)
            bot.set_state(message.from_user.id, UserState.hotels_count, message.chat.id)
            bot.send_message(chat_id=message.chat.id, text='Укажите дату заезда в отель.')
            get_check_in_out_date(message)
    else:
        msg = bot.send_message(chat_id=message.chat.id, text='Укажите количество цифрами.')
        bot.register_next_step_handler(message=msg, callback=get_hotels_count)


@logger.catch
def add_photo(message: types.Message) -> None:
    """
    Функция. Принимает от пользователя количество фотографий.
    :param message сообщение пользователя с количеством фотографий отеля.
    :return None
    """

    if message.text == '/help':
        cancel_request(message)
        return

    if message.text.isdigit():
        if not 5 >= int(message.text) > 0:
            logger.info(f'User {message.chat.id} chose wrong number of photos.')
            msg = bot.send_message(chat_id=message.chat.id, text='Указано некорректное значение.')
            bot.register_next_step_handler(message=msg, callback=add_photo)
            return
        else:
            logger.info(f'Set number of photos from user {message.chat.id} request')
            chat_id = message.chat.id
            set_info(column='photos_count', value=message.text, user_id=chat_id)
            bot.set_state(message.from_user.id, UserState.photos_count, message.chat.id)
            result(user_id=chat_id)
            help_message(message)
    else:
        msg = bot.send_message(chat_id=message.chat.id, text='Укажите количество цифрами.')
        bot.register_next_step_handler(message=msg, callback=add_photo)


@logger.catch
@bot.callback_query_handler(func=lambda call: True)
def reg_city_choice(call: types.CallbackQuery) -> None:
    """
    Функция. Обрабатывает ответ пользователя, введенный с клавиатуры телеграм бота.
    :param call: ответ на выбор населенного пункта для поиска, ответ на вопрос о необходимости выгрузки фотографий.
    :return: None
    """
    if call.data == 'No':
        logger.info(f'User {call.from_user.id} choose request without photo.')
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        set_info(column='photos_count', value=0, user_id=call.from_user.id)
        result(user_id=call.from_user.id)
        help_message(call.message)
    elif call.data == 'Yes':
        logger.info(f'User {call.from_user.id} choose request with photo.')
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        msg = bot.send_message(chat_id=call.from_user.id, text='Укажите кол-во фотографий (не более 5).')
        bot.register_next_step_handler(message=msg, callback=add_photo)
    elif call.data == 'help':
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        cancel_request(call.message)
        return
    else:
        logger.info(f"User {call.from_user.id} choose city {call.data.split('|')[0]}")
        set_info(column='city_id', value=int(call.data), user_id=call.from_user.id)
        set_info(column='city_name', value=str(call.data), user_id=call.from_user.id)
        bot.send_message(chat_id=call.from_user.id, text=call.data.split('|')[0])
        command_check = get_info(user_id=call.from_user.id)
        bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id)
        if command_check[1] == 'bestdeal':
            msg = bot.send_message(chat_id=call.from_user.id, text='Введите диапазон цен в рублях через пробел.')
            from handlers.custom_heandlers.best_deal import price_range
            bot.register_next_step_handler(message=msg, callback=price_range)
        else:
            msg = bot.send_message(chat_id=call.from_user.id, text='Сколько отелей ищем (не более 25)?')
            bot.register_next_step_handler(message=msg, callback=get_hotels_count)
