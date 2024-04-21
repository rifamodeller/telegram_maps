from telebot import types
import telebot
from geo import geocode, load_map, capitals_europe
import random

bot = telebot.TeleBot(Token)

information = ''
otvets = 0
goagain = True


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yess = types.KeyboardButton('/Давай начнем')
    no = types.KeyboardButton('/Нет, может позже')
    markup.add(yess, no)
    mess = f'''Привет, {message.from_user.first_name}.
    Я хочу помочь тебе выучить страны и столицы мира'''
    bot.send_message(message.chat.id, mess, reply_markup=markup)


@bot.message_handler()
def text(message):
    if message.text == '/Давай начнем':
        while otvets != 10:
            if goagain:
                yes(message)
    if message.text == '/Нет, может позже':
        bot.send_message(message.chat.id, 'Прискорбно, тогда увидимся потом')


@bot.message_handler()
def returnn(message):
    global otvets
    global goagain
    if information.lower() == message.text.lower():
        bot.send_message(message.chat.id, 'Ответ верен')
        otvets += 1
        goagain = True
    else:
        bot.send_message(message.chat.id, 'Ответ неверен')
        otvets += 1
        goagain = True


@bot.message_handler()
def yes(message):
    global goagain
    goagain = False
    bot.send_message(message.chat.id, 'Как называется эта страна?')
    i = random.randint(0, 9)
    global information
    information = capitals_europe[i]
    print(information)
    load_map(geocode(capitals_europe[i]))
    with open('map.png', 'rb') as file:
        bot.send_photo(message.chat.id, file)
    bot.register_next_step_handler(message, returnn)


bot.polling(none_stop=True)
