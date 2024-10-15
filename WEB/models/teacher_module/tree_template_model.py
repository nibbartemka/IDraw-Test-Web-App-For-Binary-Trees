from __future__ import annotations
from pandas import read_sql


def get_tree_type(connection: Connection) -> DataFrame:
    '''
        Функция для получения датафрейма с данными таблицы tree_type
    '''

    return read_sql(
        '''
            SELECT
                *
            FROM
                tree_type
        ''',
        connection
    )


def get_key_template(connection: Connection) -> DataFrame:
    '''
        Функция для получения датафрейма с данными таблицы key_template
    '''
    return read_sql(
        '''
            SELECT
                *
            FROM
                key_template
        ''',
        connection
    )


def get_tree_template(connection: Connection, tree_template_id) -> DataFrame:
    '''
        Функция для получения записи о шаблоне дерева с заданным tree_template_id
    '''

    return read_sql(
        f'''
            SELECT
                *
            FROM
                tree_template
            WHERE
                tree_template_id = {tree_template_id}
        ''',
        connection
    )

def check_tree_template_include(connection: Connection, tree_template_id: int) -> list:
    '''
        Функция для проверки включаения шаблона дерева в шаблон тестового задания
    '''
    cursor = connection.cursor()
    cursor.execute(
        f'''
            SELECT
                task_template_id
            FROM
                task_template
            WHERE
                tree_template_id = {tree_template_id}
        '''
    )

    task_template_id = cursor.fetchall()

    if task_template_id:
        return [
            'tree_type_id',
            'key_template_id',
            'tree_height',
            'node_count'
        ]
    
    return []


def update_tree_template(connection: Connection, tree_template_id: int, data: list[Any]) -> None:
    '''
        Функция для обновления шаблона дерева
    '''
    cursor = connection.cursor()

    cursor.execute(
        f'''
            UPDATE tree_template
            SET
                tree_type_id = ?, 
                key_template_id = ?, 
                tree_template_height = ?, 
                tree_template_keys_amount = ?, 
                tree_structure = ?, 
                tree_template_difficulty = ?
            WHERE
                tree_template_id = {tree_template_id}
        ''',
        data
    )
    connection.commit()


def update_difficulty(connection: Connection,  tree_template_id: int, data: int) -> None:
    '''
        Функция для обновления шаблона дерева
    '''
    cursor = connection.cursor()

    cursor.execute(
        f'''
            UPDATE tree_template
            SET
                tree_template_difficulty = {data}
            WHERE
                tree_template_id = {tree_template_id}    
        '''
    )
    connection.commit()
    

def del_tree_template(connection: Connection, tree_template_id: int) -> int|None:
    '''
        Функция для удаления шаблона дерева
    '''
    cursor = connection.cursor()
    
    cursor.execute(
        f'''
            DELETE FROM tree_template
            WHERE
                tree_template_id = {tree_template_id}   
        '''
    )
    connection.commit()
    
    return cursor.rowcount



def add_tree_template(connection: Connection, data: list[Any]) -> int|None:
    '''
        Функция для добавления шаблона дерева
    '''

    cursor = connection.cursor()
    cursor.execute(
        '''
            SELECT
                tree_template_id
            FROM
                tree_template
            WHERE
                tree_type_id = ? AND
                key_template_id = ? AND
                tree_template_height = ? AND
                tree_template_keys_amount = ? AND 
                tree_structure = ?
        ''',
        data[:-2]
    )

    tree_template_id = cursor.fetchone()
    if tree_template_id:
        return None

    cursor.execute(
        f'''
            INSERT INTO tree_template (
                tree_type_id, 
                key_template_id, 
                tree_template_height, 
                tree_template_keys_amount, 
                tree_structure,
                tree_template_difficulty, 
                teacher_id
            )
            VALUES 
                {tuple(data)}
        '''
    )
    connection.commit()
    
    return cursor.lastrowid