# -*- coding: utf8 -*-
from telebot.handler_backends import State, StatesGroup


class UserState(StatesGroup):
    """Класс состояний пользователя"""
    command = State()
    hotels_count = State()
    price_min = State()
    price_max = State()
    distance_min = State()
    distance_max = State()
    checkIn = State()
    checkOut = State()
    photos_count = State()
    request_time = State()
    city_id = State()
    city_name = State()
