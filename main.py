# noinspection PyUnresolvedReferences
import telebot
import logging
from config import TG_TOKEN, VK_PUBLICS_LIST
from vk_module import get_public_updates

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я буду присылать новые \nкомнаты в центре, подписывайся на рассылку.")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['start', 'help'])
def parse_vk(message):
    wall_data = []
    for public_id in VK_PUBLICS_LIST:
        wall_data += get_public_updates(public_id)

    bot.send_message(message.chat.id, )


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
bot.polling()
