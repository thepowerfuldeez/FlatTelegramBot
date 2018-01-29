# noinspection PyUnresolvedReferences
import telebot
import logging
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
bot.polling()
