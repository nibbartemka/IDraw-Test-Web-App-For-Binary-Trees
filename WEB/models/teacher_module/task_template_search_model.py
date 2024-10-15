from __future__ import annotations
from pandas import read_sql
from typing import TypeAlias
from app import SEPARATOR


DataList: TypeAlias = list[tuple[int, str]]

def get_key_templates(connection: Connection) -> DataList:
    '''
        Функция для получения списка, состоящего из кортежей, обозначающих id и name типа ключа
    '''

    cursor = connection.cursor()
    cursor.execute(
        '''
            SELECT
                key_template_id,
                key_template_name
            FROM
                key_template
        '''
    )

    return cursor.fetchall()


def get_tree_types(connection: Connection) -> DataList:
    '''
        Функция для получения списка, состоящего из кортежей, обозначающих id и name типа дерева
    '''

    cursor = connection.cursor()
    cursor.execute(
        '''
            SELECT
                tree_type_id,
                tree_type_name
            FROM
                tree_type
        '''
    )

    return cursor.fetchall()


def get_operation_template(connection: Connection) -> DataList:
    '''
        Функция для получения списка, состоящего из кортежей, обозначающих name шаблона операции
    '''

    cursor = connection.cursor()
    cursor.execute(
        '''
            SELECT
                operation_name
            FROM
                operation_template
            GROUP BY
                operation_name
        '''
    )

    return tuple(
        map(
            lambda item: item[0],
            cursor.fetchall()
        )
    )


def get_formula_task(connection: Connection, formula_task: dict[int, dict]) -> DataList:
    '''
        Функция для получения списка, состоящего из кортежей, 
        обозначающих id и url-картинки формулы тестового задания
    '''
    
    cursor = connection.cursor()
    cursor.execute(
        '''
            SELECT
                formula_task_id
            FROM
                formula_task
        '''
    )

    return tuple(
        map(
            lambda item: (item[0], formula_task.get(item[0]).get('picture')),
            cursor.fetchall()
        )
    )
    

def get_my_task_templates(connection: Connection,  
                            teacher_id: int, 
                            tree_height: tuple[int], 
                            node_count_min: int, 
                            node_count_max: int,
                            key_templates_ids: tuple[int], 
                            tree_types_ids: tuple[int],
                            operation_template: tuple[str],
                            formula_task: tuple[int],
                            difficulty_min: float,
                            difficulty_max: float,
                            # exclude_task_template: tuple[int]
                            ) -> DataFrame:
    '''
        Функция для получения DataFrame, 
        включащего отфильтрованную информацию о шаблонах деревьев, 
        созданных определенным преподавателем
    '''

    # exclude_tasks = f"AND task_template_id NOT IN {(*exclude_task_template, exclude_task_template[0])}" if exclude_task_template else ''

    return read_sql(
        f'''
            SELECT
                task_template_id,
                task_template_id || '-' || tree_structure AS task_template_identifier,
                operation_name || '{SEPARATOR}' || tree_type_name || '{SEPARATOR}' || key_template_name || '{SEPARATOR}' || tree_template_height || '{SEPARATOR}' || tree_template_keys_amount || '{SEPARATOR}' || task_template_difficulty AS task_template_description
            FROM
                task_template JOIN
                tree_template USING (tree_template_id) JOIN
                key_template USING (key_template_id) JOIN
                tree_type USING (tree_type_id) JOIN
                operation_template USING (operation_template_id)
            WHERE
                tree_template.tree_type_id IN {tree_types_ids} AND
                tree_template_height IN {tree_height} AND
                tree_template_keys_amount BETWEEN {node_count_min} AND {node_count_max} AND
                key_template_id IN {key_templates_ids} AND
                task_template_difficulty BETWEEN {difficulty_min} AND {difficulty_max} AND
                task_template.teacher_id = {teacher_id} AND
                formula_task_id IN {formula_task} AND
                operation_name IN {operation_template}
            ORDER BY
                task_template_id DESC
        ''',
        connection
    )


def get_other_task_templates(connection: Connection,  
                            teacher_id: int, 
                            tree_height: tuple[int], 
                            node_count_min: int, 
                            node_count_max: int,
                            key_templates_ids: tuple[int], 
                            tree_types_ids: tuple[int],
                            operation_template: tuple[str],
                            formula_task: tuple[int],
                            difficulty_min: float,
                            difficulty_max: float,
                            # exclude_task_template: tuple[int]
                            ) -> DataFrame:
    '''
        Функция для получения DataFrame, 
        включащего отфильтрованную информацию о шаблонах деревьев, 
        созданных остальными преподавателями
    '''

    # exclude_tasks = f"AND task_template_id NOT IN {(*exclude_task_template, exclude_task_template[0])}" if exclude_task_template else ''

    return read_sql(
        f'''
            SELECT
                task_template_id,
                task_template_id || '-' || tree_structure AS task_template_identifier,
                operation_name || '{SEPARATOR}' || tree_type_name || '{SEPARATOR}' || key_template_name || '{SEPARATOR}' || tree_template_height || '{SEPARATOR}' || tree_template_keys_amount || '{SEPARATOR}' || task_template_difficulty AS task_template_description
            FROM
                task_template JOIN
                tree_template USING (tree_template_id) JOIN
                key_template USING (key_template_id) JOIN
                tree_type USING (tree_type_id) JOIN
                operation_template USING (operation_template_id)
            WHERE
                tree_template.tree_type_id IN {tree_types_ids} AND
                tree_template_height IN {tree_height} AND
                tree_template_keys_amount BETWEEN {node_count_min} AND {node_count_max} AND
                key_template_id IN {key_templates_ids} AND
                task_template_difficulty BETWEEN {difficulty_min} AND {difficulty_max} AND
                task_template.teacher_id <> {teacher_id} AND
                formula_task_id IN {formula_task} AND
                operation_name IN {operation_template}
            ORDER BY
                task_template_id DESC
        ''',
        connection
    )