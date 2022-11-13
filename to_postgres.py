# -*- coding: utf-8 -*-
import psycopg2
from psycopg2 import Error
from config import *


def execute_read_query(query):
    result = None
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # #Дополнителльные сведения
        # print(f"Database - {DATABASE} opened successfully")
        # # Распечатать сведения о PostgreSQL
        # print("Информация о сервере PostgreSQL")
        # print(connection.get_dsn_parameters(), "\n")
        # # Выполнение SQL-запроса
        # cursor.execute("SELECT version();")
        # # Получить результат
        # record = cursor.fetchone()
        # print("Вы подключены к - ", record, "\n")
        # Выполнение основного запроса
        cursor.execute(query)
        result = cursor.fetchall()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            # print("Соединение с PostgreSQL закрыто")
    return result


def aphorism_by_id(id):
    query = f'''select id , meta , "content", autor from {table} a where id = {id};'''
    res = execute_read_query(query)
    result = res[0]
    return result

# Поиск по одному полю
def list_id(field='meta', search=''):
    if field in ['meta', 'autor','"content"']:
        query = f'''select id
                    from {table} a
                    where {field} ilike '%{search}%' ;'''
        _list = execute_read_query(query)
        id_list = [_id[0] for _id in _list]
        return id_list

# Поиск по всем полям
def list_id_all(data_search=''):
    query = f'''select id
                from {table} a
                where meta ilike '%{data_search}%' or
                 autor ilike '%{data_search}%' or
                 "content" ilike '%{data_search}%';'''
    _list = execute_read_query(query)
    id_list = [_id[0] for _id in _list]
    return id_list


