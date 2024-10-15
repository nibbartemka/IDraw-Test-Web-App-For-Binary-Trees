import sqlite3

DB_DUMP_PATH = 'db_dump.txt'


def db_init(cursor):
    with open(DB_DUMP_PATH, 'r', encoding='UTF-8') as input_file:
        dump = input_file.read()

    cursor.executescript(dump)


def get_db_connection(database_name):
    return sqlite3.connect(database_name)


formula_task = {
    1: {
        'picture': '/static/pictures/formula_task_1.png', 
        'args': [{'n': int}, {'mi_s': list}]
    },
}

formula_test = {
    1: {
        'picture': '/static/pictures/formula_test_1.png',
        'args': [{'B': int, 'ri_s': list, 'zi_s': list}]
    }
}