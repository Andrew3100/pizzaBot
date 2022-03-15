from db import *
import telebot
from telebot import *
# Подключаем базу
DB = connect_to_db(connect)


bot = telebot.TeleBot('5172890739:AAGvRGygRXTX_8vUNLu92oe567ajhsS41aQ')


@bot.message_handler(commands=['start', 'help'])
def send_welcome_message(message):
    with DB.cursor() as db:
        check_new = f"SELECT * FROM users WHERE username = '{message.from_user.username}'"
        check = db.execute(check_new)
        if check == 0:
            create_user_sql = f"INSERT INTO users (telegram_nik,username) VALUES ('{message.from_user.first_name}','{message.from_user.username}')"
            db.execute(create_user_sql)
            DB.commit()
    keyboard = types.InlineKeyboardMarkup()
    table = types.InlineKeyboardButton(text='Забронировать столик', callback_data='table')
    pizza = types.InlineKeyboardButton(text='Заказать пиццу', callback_data='pizza')
    keyboard.add(table)
    keyboard.add(pizza)
    bot.reply_to(message,f'Привет, {message.from_user.first_name}. Я бот Secret Pizza Lab. Могу помочь тебе заказать пиццу 🍕 или забронировать столик 🥂', reply_markup=keyboard)



@bot.message_handler(func=lambda m: True)
def send_welcome_message(message):
    bot.reply_to(message, message.text)

bot.polling()


