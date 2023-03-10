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

@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Добавить заправку")
    btn2 = types.KeyboardButton("Добавить расходы")
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой транспортный бот!", reply_markup=markup)

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