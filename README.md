# Инструкция по использованию TelegramHotelBot
## Запуск
### TOKEN_BOT

Для взаимодействия вашего бота с вашим ботом телеграм вам нужно создать файл .env в корне каталога и добавить туда строку
TOKEN_BOT = здесь вам нужно написать ваш токен

### TOKEN_API
Для взаимодействия вашего бота с API базой Hotels.com следует в файл .env в корне каталога добавить строку

TOKEN_API = здесь вам нужно написать ваш токен

### Установка библиотек
Для установки библиотек введите в консоли
```
pip install -r requirements.txt
```
### Ваш бот готов к использованию
## Взаимодействие c ботом
### Чтобы бот начал с вами общение, вам нужно ввести одну из двух команд: /start или /help. 
При подключении к боту и вводу команды */start*, бот выведет приветственное сообщение, чтобы
получить приветственную аватарку, необходимо в папку *welcome_jpg* поместить соответсвующую
картинку и назвать ее *welcome.jpg*. 
Вторым сообщением выведет список доступных команд.
### /help
При вводе команды выведет список доступных команд.

### /lowprice
Команда запрашивает информацию у пользователя и выводит список отелей, сортированных по цене. Сначала идут самые дешевые.
1. При вводе команды запросит у пользователя:
    1. Город, в котором будет производиться поиск отеля.
    2. Запросит у пользователя количество отелей, которое нужно вывести.
    3. Выведет клавиатуру-календарь, в которой пользователь должен указать дату заезда и выезда в отель.
    4. Спросит у пользователя, нужно ли ему показывать фотографии отелей и если нужно, то сколько.
2. После обработки ответов от пользователя выведет информацию по каждому найденному отелю в формате:
    1. Сообщение с фотографиями отеля (если требуется).
    2. Сообщение и информацией об отеле:
        1. Название отеля.
        2. Адрес отеля.
        3. Рейтинг отеля.
        4. Удаленность отеля от центра города.
        5. Цена за ночь.
        6. Цена за весь срок пребывания.
        8. Ссылка на сайт отеля.

### /highprice
Команда запрашивает информацию у пользователя и выводит список отелей, сортированных по цене. Сначала идут самые дорогие.
1. При вводе команды запросит у пользователя:
    1. Город, в котором будет производиться поиск отеля.
    2. Запросит у пользователя количество отелей, которое нужно вывести.
    3. Выведет клавиатуру-календарь, в которой пользователь должен указать дату заезда и выезда в отель.
    4. Спросит у пользователя, нужно ли ему показывать фотографии отелей и если нужно, то сколько.
2. После обработки ответов от пользователя выведет информацию по каждому найденному отелю в формате:
    1. Сообщение с фотографиями отеля (если требуется).
    2. Сообщение и информацией об отеле:
        1. Название отеля.
        2. Адрес отеля.
        3. Рейтинг отеля.
        4. Удаленность отеля от центра города.
        5. Цена за ночь.
        6. Цена за весь срок пребывания.
        7. Ссылка на сайт отеля.
### /bestdeal
Команда запрашивает информацию у пользователя и выводит список отелей, сортированных по цене (первыми идут самые дешевые)
и по расстоянию от центра города. 
1. При вводе команды запросит у пользователя:
    1. Город, в котором будет производиться поиск отеля.
    2. Запросит минимальную и максимальную стоимость в рублях.
    3. Запросит минимальную и максимальную удаленность отеля от центра города в км.
    4. Запросит у пользователя количество отелей, которое нужно вывести.
    5. Выведет клавиатуру-календарь, в которой пользователь должен указать дату заезда и выезда.
    7. Спросит у пользователя, нужно ли ему показывать фотографии отелей и если нужно, то сколько.
2. После обработки ответов от пользователя выведет информацию по каждому найденному отелю в формате:
    1. Сообщение с фотографиями отеля (если требуется).
    2. Сообщение и информацией об отеле:
        1. Название отеля.
        2. Адрес отеля.
        3. Рейтинг отеля.
        4. Удаленность отеля от центра города.
        5. Цена за ночь.
        6. Цена за весь срок пребывания.
        7. Ссылка на сайт отеля.
### /history
Отправляет пользователю его историю поиска, если таковая имеется.
1. Название введенной пользователем команды.
2. Время начала поиска.
3. Список названий найденных отелей по запросу.
