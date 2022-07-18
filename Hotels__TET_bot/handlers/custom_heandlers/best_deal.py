from loguru import logger
from telebot import types

from database.chat_users_db import set_info
from handlers.default_heandlers.start_help import cancel_request
from keyboards.reply.keyboard_reply import get_hotels_count

from loader import bot
from states.user_states import UserState


@logger.catch
def price_range(message: types.Message) -> None:
    """
    Функция. Принимает диапазон цен для поиска отелей в рамках команды /bestdeal.
    :param message: сообщение пользователя с диапазоном цен.
    :return: None
    """
    if message.text == '/help':
        cancel_request(message)
        return

    price_params = message.text.split()

    if len(price_params) != 2:
        logger.info(f'User {message.chat.id} input wrong price range.')
        msg = bot.send_message(chat_id=message.chat.id, text='Диапазон цен указан некорректно.\n'
                                                             'Укажите минимальную и максимальную '
                                                             'цены в рублях через пробел.')
        bot.register_next_step_handler(message=msg, callback=price_range)
        return

    try:
        if int(price_params[0]) > int(price_params[1]):
            price_params[0], price_params[1] = price_params[1], price_params[0]
        chat_id = message.chat.id
        set_info(column='price_min', value=int(price_params[0]), user_id=chat_id)
        set_info(column='price_max', value=int(price_params[1]), user_id=chat_id)
    except ValueError:
        msg = bot.send_message(chat_id=message.chat.id, text='Укажите значения цен цифрами.')
        bot.register_next_step_handler(message=msg, callback=price_range)
    else:
        logger.info(f'User {message.from_user.id} pick {message.text} as price range.')
        bot.send_message(chat_id=message.chat.id, text=f'Установлен диапазон: '
                                                       f'минимальная цена - {price_params[0]}, '
                                                       f'максимальная цена - {price_params[1]}.')
        msg = bot.send_message(chat_id=message.chat.id, text='Укажите через пробел диапазон расстояния, '
                                                             'в котором должен находиться отель от центра '
                                                             '(в километрах).')
        bot.register_next_step_handler(message=msg, callback=distance_range)


@logger.catch
def distance_range(message: types.Message) -> None:
    """
    Функция. Принимает диапазон расстояния удаленности отелей от центра города
    в рамках команды /bestdeal.
    :param message: сообщение пользователя с диапазоном расстояния.
    :return: None
    """
    if message.text == '/help':
        cancel_request(message)
        return

    distance_params = message.text.split()

    if len(distance_params) != 2:
        logger.info(f'User {message.chat.id} input wrong distance range.')
        msg = bot.send_message(chat_id=message.chat.id, text='Диапазон указан некорректно.\n'
                                                             'Укажите минимальное и максимальное '
                                                             'расстояние через пробел (в км).')
        bot.register_next_step_handler(message=msg, callback=distance_range)
        return

    try:
        if int(distance_params[0]) > int(distance_params[1]):
            distance_params[0], distance_params[1] = distance_params[1], distance_params[0]

        chat_id = message.chat.id
        set_info(column='distance_min', value=int(distance_params[0]), user_id=chat_id)
        set_info(column='distance_max', value=int(distance_params[1]), user_id=chat_id)
        bot.set_state(message.from_user.id, UserState.distance_min, message.chat.id)
        bot.set_state(message.from_user.id, UserState.distance_max, message.chat.id)
    except ValueError:
        msg = bot.send_message(chat_id=message.chat.id, text='Укажите значения расстояния цифрами.')
        bot.register_next_step_handler(message=msg, callback=distance_range)
    else:
        logger.info(f'User {message.from_user.id} pick {message.text} as distance range.')
        bot.send_message(chat_id=message.chat.id, text=f'Установлен диапазон: '
                                                       f'минимальное расстояние - {distance_params[0]}, '
                                                       f'максимальное расстояние - {distance_params[1]}.')
        msg = bot.send_message(chat_id=message.chat.id, text='Сколько отелей ищем (не более 25)?')
        bot.register_next_step_handler(message=msg, callback=get_hotels_count)
