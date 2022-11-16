# -*- coding: utf-8 -*-
import random
# from to_postgres import aphorism_by_id, list_id, list_id_all
from to_sqlite import aphorism_by_id, list_id, list_id_all

class listing():
    # listing_id = {}
    def __init__(self):
        self.field = {}
        self.data_search = {}
        self.listing_id = {}

    def new_user(self, user_id):
        if not user_id in self.field:
            self.field[user_id] = ''
        if not user_id in self.data_search:
            self.data_search[user_id] = ''
        if not user_id in self.listing_id:
            self.listing_id[user_id] = ''


# Выбрать Id
    def random_id(self, user_id):
        result = ''
        if self.listing_id[user_id]:
            result = random.choice(self.listing_id[user_id])
            self.listing_id[user_id].remove(result)
        return (result)


    # Подготовка полей для печати
    def print_aphorism_by_id(self, Id, user_id):
        _aphorism = aphorism_by_id(Id)
        text_info = len(self.listing_id[user_id])
        content = {
                    'info':text_info,
                    'meta':_aphorism[1],
                    'content':_aphorism[2],
                    'autor':_aphorism[3],
        }
        return content

    # Поиск по базе и вывод list_id
    def create_id_list(self,user_id):
        _field = self.field[user_id]
        _search = self.data_search[user_id]
        if _field == 'meta' or _field == 'autor':
            _LIST = list_id(field=_field, search=_search)
        elif _field == 'content':
            _LIST = list_id(field='aphorism', search=_search) # for sqlite
            # _LIST = list_id(field='"content"', search=_search) # for postgres
        elif _field == 'all':
            _LIST = list_id_all(data_search=_search)
        else:
            _LIST = list_id()
        self.listing_id[user_id] = _LIST

