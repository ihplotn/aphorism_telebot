# -*- coding: utf-8 -*-
import logging
import telebot
from telebot import types, apihelper
from config import tkn
from engine import listing
import time
from datetime import date

apihelper.ENABLE_MIDDLEWARE = True

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

@bot.middleware_handler(update_types=['message', 'callback_query'])
def set_session(bot_instance, message):
    ls.new_users(str(message.from_user.id))

def markup():
    _markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    btn_aphorism = types.KeyboardButton('/aphorism')
    btn_search = types.KeyboardButton('/search')
    btn_next = types.KeyboardButton('/next')
    btn_help = types.KeyboardButton('/help')
    _markup.add(btn_aphorism, btn_search, btn_next, btn_help)
    return _markup

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

    bot.send_message(message.chat.id, content, parse_mode='html', reply_markup=markup())


# TODO Помощь уточнить описание
@bot.message_handler(commands=['help'])
def help(message):
    content = f'<b>Описание работы бота</b>\n\n' \
              f'Для взаиммодействия с ботом используйте следующие команды: \n' \
              f'/aphorism - показать случайный афоризм (поиск сбрасывается)\n' \
              f'/search - поиск по автору, теме или по тексту афоризма\n' \
              f'/next - показать следующий афоризм из выбраных поиском\n'

    bot.send_message(message.chat.id, content, parse_mode='html', reply_markup=markup())


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
    ls.users[str(query.from_user.id)]['field'] = FIELD
    text_field = f'Введите слово для поиска {_field}:'
    bot.send_message(query.message.chat.id, text_field, parse_mode='html')


# Блок NEXT вывод следующего id() из списка
@bot.message_handler(commands=['next'])
def next_aphorism(message):
    user_id = str(message.from_user.id)
    content = ls.next_aphorism_content(user_id)
    log.info(f"{content[1]}")
    bot.send_message(message.chat.id, content[0], parse_mode='html', reply_markup=markup())


# Блок APHORISM брос всей поисковых запросов, вывод случайного id() из полного списка
@bot.message_handler(commands=['aphorism'])
def aphorism_rand(message):
    user_id = str(message.from_user.id)
    ls.new_users(user_id, new_list=True)
    next_aphorism(message)


# Блок обработка текста пользователя
@bot.message_handler()
def any_mess(message):
    user_id = str(message.from_user.id)
    ls.users[user_id]['search_data'] = str(message.text)
    ls.create_id_list(user_id)
    next_aphorism(message)



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