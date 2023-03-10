import telebot
from telebot import types
import sqlite3


conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()    

def db_automobiles():
    automobiles = cursor.execute('SELECT * FROM automobile')
    conn.commit()
    return automobiles


bot = telebot.TeleBot('6038960334:AAGWbNJipCHuPPytvZ5FnZaey_8IsgRZ6RA')
user_data = []

@bot.message_handler(commands=['reg'])
def reg(message):
    bot.send_message(message.chat.id, 'Введите имя:')
    bot.register_next_step_handler(message, firstname)
    
def firstname(message):
    bot.send_message(message.chat.id, 'Введите фамилию:')
    user_data.append(message.text)
    bot.register_next_step_handler(message, phone)

def phone(message):
    bot.send_message(message.chat.id, 'Введите телефон в формате 89...:')
    user_data.append(message.text)
    bot.register_next_step_handler(message, print_user_data)

def print_user_data(message):
    user_data.append(message.text)
    print(user_data)
    bot.send_message(message.chat.id, 'Добро пожаловать ' + user_data[0] + ' ' + user_data[1])
    bot.register_next_step_handler(message, start)

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text = "Добавить заправку", callback_data = 'no')
    btn2 = types.InlineKeyboardButton(text = "Добавить расходы", callback_data='no')
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой транспортный бот!", reply_markup=markup)
    print(message.from_user.id)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Добавить заправку':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
        automobiles = db_automobiles()
        for automobile in automobiles:
            btn = types.KeyboardButton(automobile[2] + ' / ' + automobile[1])
            markup.add(btn)
        bot.send_message(message.from_user.id, 'Выберите автомобиль', reply_markup=markup) #ответ бота


    elif message.text == 'Как стать автором на Хабре?':
        bot.send_message(message.from_user.id, 'Вы пишете первый пост, его проверяют модераторы, и, если всё хорошо, отправляют в основную ленту Хабра, где он набирает просмотры, комментарии и рейтинг. В дальнейшем премодерация уже не понадобится. Если с постом что-то не так, вас попросят его доработать.\n \nПолный текст можно прочитать по ' + '[ссылке](https://habr.com/ru/sandbox/start/)', parse_mode='Markdown')

    elif message.text == 'Правила сайта':
        bot.send_message(message.from_user.id, 'Прочитать правила сайта вы можете по ' + '[ссылке](https://habr.com/ru/docs/help/rules/)', parse_mode='Markdown')

    elif message.text == 'Советы по оформлению публикации':
        bot.send_message(message.from_user.id, 'Подробно про советы по оформлению публикаций прочитать по ' + '[ссылке](https://habr.com/ru/docs/companies/design/)', parse_mode='Markdown')


bot.polling(none_stop=True, interval=0) 