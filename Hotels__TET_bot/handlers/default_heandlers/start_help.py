# -*- coding: utf8 -*-
from loguru import logger
from telebot import types

from loader import bot


@logger.catch
@bot.message_handler(commands=['start'])
def start(message: types.Message) -> None:
    """
    Функция. Выполняет команду /start.
    Приветствует пользователя (с аватаркой или без) и знакомит его со списком доступных команд.
    :param message: сообщение пользователя с командной /start
    :return: None
    """
    try:
        photo = open('welcome_jpg/welcome.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        logger.info(f'User {message.chat.id} FileNotFoundError')
    finally:
        logger.info(f'User {message.chat.id} used command /start')
        bot.send_message(chat_id=message.chat.id,
                         text=f"Добрый день, {message.from_user.first_name}!  Меня зовут Hotels__TET_bot. "
                              "Я помогу вам подобрать отель с сайта hotels.com. "
                              "Доступны следующие команды: \n"
                         )
        help_message(message)


@logger.catch
@bot.message_handler(commands=['help'])
def help_message(message: types.Message) -> None:
    """
    Функция. Выполняет команду /help.
    Знакомит пользователя со списком доступных команд.
    :param message: сообщение пользователя с командной /help
    :return: None
    """
    logger.info(f'User {message.chat.id} used command /help')
    bot.send_message(chat_id=message.chat.id, text='/help - список доступных команд или отмена текущего запроса;\n'
                                                   '/lowprice - топ самых дешевых отелей в городе;\n'
                                                   '/highprice - топ самых дорогих отелей в городе;\n'
                                                   '/bestdeal - топ отелей, '
                                                   'наиболее подходящих по цене и расположению от центра;\n'
                                                   '/history - история поиска отелей;\n')


@logger.catch
@bot.message_handler(commands=['help'])
def cancel_request(message: types.Message) -> None:
    """
    Функция, которая реагирует на команду /help.
    Отменяет текущий запрос пользователя.
    :param message: сообщение от пользователя с командой /help.
    :return: None
    """
    logger.info(f'User {message.chat.id} used command {message.text}')
    bot.send_message(chat_id=message.chat.id, text='Текущий запрос был отменен.')
    help_message(message)
