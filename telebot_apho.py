# -*- coding: utf-8 -*-
import logging
import telebot
from telebot import types
from config import tkn
from engine import listing
import time
from datetime import date


log = logging.getLogger('bot')

bot = telebot.TeleBot(tkn)

ls = listing()

def conf_logger():
    stream_hander = logging.StreamHandler()
    stream_hander.setFormatter(logging.Formatter("%(levelname)s,%(message)s"))
    log.addHandler(stream_hander)
    log.setLevel(logging.DEBUG)
    stream_hander.setLevel(logging.DEBUG)


    file_name = f'telebot_{date.today().strftime("%m_%Y")}.log'
    file_hander = logging.FileHandler(file_name)
    file_hander.setFormatter(logging.Formatter(fmt="%(asctime)s,%(levelname)s,%(message)s",  datefmt='%Y-%m-%d %H:%M:%S'))
    log.addHandler(file_hander)
    file_hander.setLevel(logging.INFO)


# TODO Старт добавить описание discription
@bot.message_handler(commands=['start'])
def start(message):
    hi = f'Здравствуйте {str(message.from_user.first_name).title()}!'
    discription = 'Описание'
    content = f'{hi}\n\n' \
              f'{discription}\n\n' \
              f'Для взаиммодействия с ботом используйте следующие команды: \n' \
              f'/aphorism - показать случайный афоризм\n' \
              f'/search - поиск по автору, теме или по тексту афоризма\n' \
              f'/next - показать следующий афоризм из поиска\n' \
              f'/help - описание работы бота\n'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    btn_aphorism = types.KeyboardButton('/aphorism')
    btn_search = types.KeyboardButton('/search')
    btn_next = types.KeyboardButton('/next')
    btn_help = types.KeyboardButton('/help')
    markup.add(btn_aphorism, btn_search, btn_next, btn_help)
    bot.send_message(message.chat.id, content, parse_mode='html', reply_markup=markup)


# TODO Помощь уточнить описание
@bot.message_handler(commands=['help'])
def help(message):
    content = f'<b>Описание работы бота</b>\n\n' \
              f'Для взаиммодействия с ботом используйте следующие команды: \n' \
              f'/aphorism - показать случайный афоризм (поиск сбрасывается)\n' \
              f'/search - поиск по автору, теме или по тексту афоризма\n' \
              f'/next - показать следующий афоризм из выбраных поиском\n'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    btn_aphorism = types.KeyboardButton('/aphorism')
    btn_search = types.KeyboardButton('/search')
    btn_next = types.KeyboardButton('/next')
    btn_help = types.KeyboardButton('/help')
    markup.add(btn_aphorism, btn_search, btn_next, btn_help)
    bot.send_message(message.chat.id, content, parse_mode='html', reply_markup=markup)


# Блок SEARСH +
@bot.message_handler(commands=['search'])
def search_aphorism(message):
    content = (f'<b>Выберите категорию поиска</b>')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton('Поиск по теме', callback_data='meta'))
    keyboard.row(types.InlineKeyboardButton('Поиск по автору', callback_data='autor'))
    keyboard.row(types.InlineKeyboardButton('Поиск по тексту афоризма', callback_data='content'))
    keyboard.row(types.InlineKeyboardButton('Поиск по всем категориям', callback_data='all'))
    bot.send_message(message.chat.id, content, parse_mode='html', reply_markup=keyboard)


# обработка SEARСH запросов
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    FIELD = query.data
    bot.answer_callback_query(query.id)  # убрать состояние загрузки
    if FIELD == 'content':
        _field = 'по тексту афоризма'
    elif FIELD == 'autor':
        _field = 'по автору'
    elif FIELD == 'meta':
        _field = 'по теме'
    else:
        FIELD = 'all'
        _field = 'по всем категориям'
    ls.field[str(query.from_user.id)] = FIELD
    text_field = f'Введите слово для поиска {_field}:'
    bot.send_message(query.message.chat.id, text_field, parse_mode='html')


# Блок NEXT вывод следующего id() из списка
@bot.message_handler(commands=['next'])
def next_aphorism(message):
    user_id = str(message.from_user.id)
    ls.new_user(user_id=user_id)
    if ls.listing_id[user_id]:
        _id = ls.random_id(user_id)
        _aphorism = ls.print_aphorism_by_id(_id,user_id)
        # print(message)
        log.info(f"{str(message.from_user.id)},{str(_id)},{ls.field[user_id]},{ls.data_search[user_id]}")
        content = f"Осталось {_aphorism['info']} афоризмов\n <b>--{_aphorism['meta']}--</b>\n{_aphorism['content']}\n\t <i>" \
                  f"~{_aphorism['autor']}</i>"

    else:
        if ls.field[user_id] == '' or ls.data_search[user_id] == '':
            content = f'<b>Все афоризмы</b>'
            aphorism_rand(message)
        else:
            content = f'<b>По Вашему запросу ничего не найдено</b>'
            ls.field[user_id] = ''
            ls.data_search[user_id] = ''

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    btn_aphorism = types.KeyboardButton('/aphorism')
    btn_search = types.KeyboardButton('/search')
    btn_next = types.KeyboardButton('/next')
    btn_help = types.KeyboardButton('/help')
    markup.add(btn_aphorism, btn_search, btn_next, btn_help)
    bot.send_message(message.chat.id, content, parse_mode='html', reply_markup=markup)


# Блок APHORISM брос всей поисковых запросов, вывод случайного id() из полного списка
@bot.message_handler(commands=['aphorism'])
def aphorism_rand(message):
    user_id = str(message.from_user.id)
    ls.new_user(user_id)
    ls.field[user_id] = ''
    ls.data_search[user_id] = ''
    ls.create_id_list(user_id)
    next_aphorism(message)


# Блок обработка текста пользователя
@bot.message_handler()
def any_mess(message):
    user_id = str(message.from_user.id)
    ls.new_user(user_id)
    if message.text:
        _text = str(message.text)
        _text.replace('"', '')
        _text.replace("'", '')
        ls.data_search[user_id] = _text
        ls.create_id_list(user_id)
        next_aphorism(message)
    elif ls.listing_id[user_id]:
        next_aphorism(message)
    else:
        aphorism_rand(message)


def telegram_polling():
    try:
        log.debug('Telebot запущен.\n Чтобы остановить скрипт нажмите Ctrl + C')
        bot.polling(none_stop=True, skip_pending=True)
    except Exception:
        # log.exception('ERROR polling')
        bot.stop_polling()
        log.debug('ERROR polling. Презапуск Telebotа.')
        ls.restart()
        time.sleep(30)
        telegram_polling()



if __name__ == "__main__":
    conf_logger()
    telegram_polling()