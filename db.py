import mysql.connector
from mysql.connector import errorcode


def db_connection(host, user, password, db_name):
    """Подключение к бд"""
    try:
        connect = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = connect.cursor()
        return cursor


def select_params(cursor, cols, table_name, param=None, value=None):
    """Запрос данных с таблицы"""
    if param:
        cursor.execute(
            "select {} from {} where {} = '{}'".format(cols, table_name, param, value))
        result = cursor.fetchall()[0]
        return result
    else:
        cursor.execute(
            "select {} from {}".format(cols, table_name))
        result = cursor.fetchall()[0]
        return result

