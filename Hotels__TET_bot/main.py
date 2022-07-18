import keyboards
from handlers.custom_heandlers import low_high_price
from keyboards.reply import keyboard_reply
from loader import bot
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
from loguru import logger

logger.add("log.log", format="{time} {level} {message}", level="INFO", rotation="10 MB", compression="zip")


if __name__ == '__main__':
    bot.add_custom_filter(StateFilter(bot))
    keyboard_reply.bot.message_handler()
    set_default_commands(bot)
    bot.infinity_polling()
