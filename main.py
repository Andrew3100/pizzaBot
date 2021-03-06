from db import *
import telebot
from telebot import *
# Подключаем базу
DB = connect_to_db(connect)


bot = telebot.TeleBot('5172890739:AAGvRGygRXTX_8vUNLu92oe567ajhsS41aQ')


@bot.message_handler(commands=['start', 'help'])
def send_welcome_message(message):
    # print(message)
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
        keyboard.add(pizza, table)
        bot.reply_to(message,
                     f'Привет, {message.from_user.first_name}. Я сотрудник Secret Pizza Lab. Могу помочь тебе заказать пиццу 🍕 или забронировать столик 🥂',
                     reply_markup=keyboard)



@bot.callback_query_handler(func=lambda call: True)
# Обработчик заказа пиццы
def pizza_order(call):
    if call.data == 'pizza':
        keyboard = types.InlineKeyboardMarkup()
        pizza_name = types.InlineKeyboardButton(text='Знаю название пиццы!', callback_data='pizza_name')
        ingredient = types.InlineKeyboardButton(text='Давай выберем по ингридиентам!', callback_data='ingredient')
        keyboard.add(pizza_name)
        keyboard.add(ingredient)
        bot.send_message(call.message.chat.id, 'Знаешь какую пиццу хочешь? Или выберем по ингридиентам?', reply_markup=keyboard)
    if call.data == 'pizza_name':
        with DB.cursor() as db:
            pizza_list = f'SELECT * FROM pizza'
            pizza_list = db.execute(pizza_list)
            pizza_list = db.fetchall()
            keyboard = types.InlineKeyboardMarkup()
            for pizza in pizza_list:
                keyboard.add(types.InlineKeyboardButton(text=str(pizza['name']), callback_data=str(pizza['id']) + '_pizza_id'))
        bot.send_message(call.message.chat.id, 'Хорошо, давай выберем пиццу 🍕', reply_markup=keyboard)

    if '_pizza_id' in call.data:
        id = call.data.split('_')[0]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Доставка', callback_data='delivery'))
        keyboard.add(types.InlineKeyboardButton(text='Самовывоз', callback_data='pickup'))
        bot.send_message(call.message.chat.id, f'Теперь давай определимся как ты получишь свою 🍕', reply_markup=keyboard)


    if 'delivery' in call.data or 'pickup' in call.data:
        bot.send_message(call.message.chat.id, f'Скажи нам свой номер телефона. Он пригодится для связи 😊')

    # Обработка бронирования столика
    if call.message.text == 'table':
        bot.send_message(call.message.chat.id, 'Вы выбрали бронирование столика!')


@bot.message_handler(func=lambda m: True)
def tel(message):
    if '8' in str(message.text) or '7' in str(message.text):
        with DB.cursor() as db:
            create_user_sql = f"UPDATE users SET telephone = '{str(message.text)}' WHERE username = '{message.from_user.username}'"
            print(create_user_sql)
            db.execute(create_user_sql)
            DB.commit()
            bot.send_message(message.chat.id, 'Спасибо, скоро мы выйдем на связь 😊')
    else:
        bot.send_message(message.chat.id, 'Ой, кажется прозошла ошибку при вводе номера 🤪. Давай ещё раз 😊')
bot.polling(none_stop=True)


