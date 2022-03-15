from db import *
import telebot
# Подключаем базу
connect_to_db(connect)


bot = telebot.TeleBot('5172890739:AAGvRGygRXTX_8vUNLu92oe567ajhsS41aQ')


@bot.message_handler(commands=['start', 'help'])
def send_welcome_message(message):
    bot.reply_to(message, 'Привет, давай работать вместе')


@bot.message_handler(func=lambda m: True)
def send_welcome_message(message):
    bot.reply_to(message, message.text)


bot.polling()


