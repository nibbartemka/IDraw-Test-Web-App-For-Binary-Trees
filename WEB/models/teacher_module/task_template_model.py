from __future__ import annotations
from pandas import read_sql


def update_task_template(connection: Connection, task_template_id: int, data: list[Any]) -> None:
    '''
        Функция для обновления шаблона тестового задания
    '''
    cursor = connection.cursor()

    cursor.execute(
        f'''
            UPDATE task_template
            SET
                tree_template_id = ?,
                formula_task_id = ?,
                operation_template_id = ?,
                task_template_difficulty = ?
            WHERE
                task_template_id = {task_template_id}
        ''',
        data
    )
    connection.commit()


def update_difficulty(connection: Connection, task_template_id: int, difficulty: float) -> None:
    '''
        Функция для обновления сложности шаблона тестового задания
    '''
    cursor = connection.cursor()

    cursor.execute(
        f'''
            UPDATE task_template
            SET
                task_template_difficulty = {difficulty}
            WHERE
                task_template_id = {task_template_id}
        '''
    )
    connection.commit()


def check_task_template_include(connection: Connection, task_template_id: int) -> list:
    '''
        Функция для проверки включения шаблона тестового задания в шаблон теста
    '''

    cursor = connection.cursor()
    cursor.execute(
        f'''
            SELECT
                test_template_id
            FROM
                test_task_template
            WHERE
                task_template_id = {task_template_id}
        '''
    )

    test_template_id = cursor.fetchall()

    if test_template_id:
        return [
            'tree_template_id',
            'operation_template_id',
            'formula_task_id',
        ]
    
    return []


def get_task_template(connection: Connection, task_template_id: int) -> DataFrame:
    '''
        Функция для получения DataFrame, содержащем информацию об определенном шаблоне тестового задания
    '''

    return read_sql(
        f'''
            SELECT
                *
            FROM    
                task_template
            WHERE
                task_template_id = {task_template_id}
        ''',
        connection
    )


def get_operations(connection: Connection, tree_type_id: int) -> DataFrame:
    '''
        Функция для получения DataFrame с операциями, которые можно проводить над деревом заданного типа
    '''

    return read_sql(
        f'''
            SELECT
                operation_template_id,
                operation_name,
                operation_text
            FROM
                operation_template
            WHERE
                tree_type_id = {tree_type_id}
        ''',
        connection
    )


def get_tree_template_data(connection: Connection, tree_template_id: int) -> DataFrame:
    '''
        Функция для получения Dataframe с информацию о шаблоне дерева
    '''
    
    return read_sql(
        f'''
            SELECT
                *
            FROM
                tree_template JOIN
                key_template USING (key_template_id) JOIN
                tree_type USING (tree_type_id)
            WHERE
                tree_template_id = {tree_template_id}
        ''',
        connection
    )


def get_formulas(connection: Connection) -> DataFrame:
    '''
        Функция для получения Dataframe с информацией о формулах тестового задания
    '''
    
    return read_sql(
        f'''
            SELECT
                *
            FROM
                formula_task
        ''',
        connection
    )


def add_task_template(connection: Connection, data: list[Any]) -> int|None:
    '''
        Функция для добавления шаблона тестового задания
    '''

    cursor = connection.cursor()

    node_index = f'AND node_index = {data[-2]}' if data[-2] else ''
    cursor.execute(
        f'''
            SELECT
                task_template_id
            FROM
                task_template
            WHERE
                tree_template_id = {data[0]} AND
                formula_task_id = {data[1]} AND
                operation_template_id = {data[2]}
                {node_index}
        '''
    )

    task_template_id = cursor.fetchone()
    if task_template_id:
        return None

    cursor.execute(
        f'''
            INSERT INTO task_template (
                tree_template_id, 
                formula_task_id, 
                operation_template_id, 
                task_template_difficulty,
                node_index,
                teacher_id
            )
            VALUES 
                {tuple(data)}
        '''
    )
    connection.commit()
    
    return cursor.lastrowid


def del_task_template(connection: Connection, task_template_id: int) -> int|None:
    '''
        Функция для удаления шаблона дерева
    '''
    cursor = connection.cursor()
    
    cursor.execute(
        f'''
            DELETE FROM task_template
            WHERE
                task_template_id = {task_template_id}   
        '''
    )
    connection.commit()
    
    return cursor.rowcount
