# -*- coding: utf-8 -*-
import random
# from to_postgres import aphorism_by_id, list_id, list_id_all
from to_sqlite import aphorism_by_id, list_id, list_id_all, full_list_id

class listing():
    FULL_LIST = full_list_id()
    COUNT_ALL =len(FULL_LIST)
    def __init__(self):
        self.users = {
            '0000':{
                'listing_id': [154,4],
                'field' : '',
                'search_data' : '',}
            }


    def new_users(self, user_id, new_list=False):
        if not user_id in self.users:
            self.users[user_id] = {
                'listing_id': '',
                'field' : '',
                'search_data' : '',}
        elif new_list:
            self.users[user_id]['listing_id'] = ''
            self.users[user_id]['field'] = ''
            self.users[user_id]['search_data'] = ''
            self.create_id_list(user_id)

    def search_parameters(self,  user_id, field='', search_data=''):
        if field:
            self.users[user_id]['field'] = field
        if search_data:
            _text = str(search_data)
            _text = _text.replace('"', '')
            _text = _text.replace("'", '')
            self.users[user_id]['search_data'] = _text

    def next_aphorism_content(self, user_id):
        if not self.users[user_id]['search_data']:
            _info = f"Всего {self.COUNT_ALL} афоризмов и цитат"
            _id = self.random_id()
            _aphorism = self.print_aphorism_by_id(_id, user_id)
            log_info = f"{user_id},{str(_id)},{self.users[user_id]['field']},{self.users[user_id]['search_data']}"
            content = f"{_info}\n <b>--{_aphorism['meta']}--</b>\n{_aphorism['content']}\n\t <i>" \
                      f"~{_aphorism['autor']}</i>"
        elif self.users[user_id]['listing_id']:
            _id = self.random_id(user_id)
            _aphorism = self.print_aphorism_by_id(_id, user_id)
            _info = f"По запросу {_aphorism['info']} афоризмов"
            log_info = f"{user_id},{str(_id)},{self.users[user_id]['field']},{self.users[user_id]['search_data']}"
            content = f"{_info}\n <b>--{_aphorism['meta']}--</b>\n{_aphorism['content']}\n\t <i>" \
                      f"~{_aphorism['autor']}</i>"

        else:
            log_info = f"{user_id},None,{self.users[user_id]['field']},{self.users[user_id]['search_data']}"
            content = f'<b>По Вашему запросу ничего не найдено</b>'
            self.new_users(user_id, new_list=True)


        return (content, log_info)

# Выбрать Id
    def random_id(self, user_id=''):
        result = ''
        if not user_id:
            result = random.choice(self.FULL_LIST)
        elif self.users[user_id]['listing_id']:
            result = random.choice(self.users[user_id]['listing_id'])
            self.users[user_id]['listing_id'].remove(result)
        return (result)


    # Подготовка полей для печати
    def print_aphorism_by_id(self, Id, user_id):
        _aphorism = aphorism_by_id(Id)
        text_info = len(self.users[user_id]['listing_id'])
        content = {
                    'info':text_info,
                    'meta':_aphorism[1],
                    'content':_aphorism[2],
                    'autor':_aphorism[3],
        }
        return content

    # Поиск по базе и вывод list_id
    def create_id_list(self, user_id):
        if not self.users[user_id]['search_data']:
            self.users[user_id]['listing_id'] = list_id()
            return
        _text = self.users[user_id]['search_data']
        _field = self.users[user_id]['field']
        if _field == 'meta':
            _LIST = list_id(field=_field, search=str(_text).upper())
        elif _field == 'autor':
            _LIST = list_id(field=_field, search=_text)
        elif _field == 'content':
            _LIST = list_id(field='aphorism', search=_text) # for sqlite
            # _LIST = list_id(field='"content"', search=_search) # for postgres
        elif _field == 'all':
            _LIST = list_id_all(data_search=_text)
        else:
            _LIST = list_id()
        self.users[user_id]['listing_id'] = _LIST

    def restart(self):
        self.users.clear()


