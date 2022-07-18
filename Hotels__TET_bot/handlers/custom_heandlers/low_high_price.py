from datetime import datetime

from loguru import logger
from telebot import types

from database.chat_users_db import create_db, set_info
from keyboards.inline.keyboard_inline import city_choice_keyboard
from loader import bot
from states.user_states import UserState


@logger.catch
@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def get_city(message: types.Message) -> None:
    """
    Функция, которая реагирует на команды /lowprice, /highprice, /bestdeal.
    Принимает от пользователя название города, в котором требуется осуществить поиск.
    :param message: сообщение пользователя с одной из команд /lowprice, /highprice, /bestdeal.
    :return: None
    """
    logger.info(f'User {message.chat.id} used command {message.text}')
    chat_id = message.chat.id
    create_db(user_id=chat_id)
    set_info(column='command', value=message.text[1:], user_id=chat_id)
    set_info(column='request_time', value=datetime.today().strftime("%X %x"), user_id=chat_id)
    set_info(column='checkIn', value=None, user_id=message.chat.id)
    set_info(column='checkOut', value=None, user_id=message.chat.id)
    msg = bot.send_message(chat_id=message.chat.id, text='Укажите в каком городе ищем отель:')
    bot.set_state(message.from_user.id, UserState.command, message.chat.id)
    bot.register_next_step_handler(message=msg, callback=city_choice_keyboard)
