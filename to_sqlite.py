# -*- coding: utf-8 -*-

import sqlite3
from sqlite3 import Error
# from config import *

DATABASE ='aphorism.db'
table = 'aphorisms'

def execute_read_query(query):
    result = None
    try:
        # Подключение к существующей базе данных
        connection = sqlite3.connect(DATABASE)
        # учет реестра для Like
        # db = SQLiteDatabase.openDatabase(...);
        # db.execSQL("PRAGMA case_sensitive_like = true;");
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Выполнение запроса
        cursor.execute(query)
        result = cursor.fetchall()
    except (Exception, Error) as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            # print("Соединение с SQLite" закрыто")
    return result


def aphorism_by_id(id):
    query = f'''select id , meta , aphorism, autor from {table} a where id = {id};'''
    res = execute_read_query(query)
    result = res[0]
    return result

# Поиск по одному полю
def list_id(field='meta', search=''):
    if field in ['meta', 'autor','aphorism']:
        query = f'''select id
                    from {table} a
                    where {field} like '%{search}%' 
                     or {field} like '%{search.lower()}%';'''
        _list = execute_read_query(query)
        id_list = [_id[0] for _id in _list]
        return id_list

# Поиск по всем полям
def list_id_all(data_search=''):
    query = f'''select id
                from {table} a
                where meta like '%{data_search.upper()}%' or
                 autor like '%{data_search}%' or autor like '%{data_search.lower()}%' or
                 aphorism like '%{data_search}%' or aphorism like '%{data_search.lower()}%';'''
    _list = execute_read_query(query)
    id_list = [_id[0] for _id in _list]
    return id_list


