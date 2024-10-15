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


def get_my_tree_templates(connection: Connection,  
                            teacher_id: int, 
                            tree_height: tuple[int], 
                            node_count_min: int, 
                            node_count_max: int,
                            key_templates_ids: tuple[int], 
                            tree_types_ids: tuple[int], 
                            difficulty_min: float,
                            difficulty_max: float) -> DataFrame:
    '''
        Функция для получения DataFrame, 
        включащего отфильтрованную информацию о шаблонах деревьев, 
        созданных определенным преподавателем
    '''

    return read_sql(
        f'''
            SELECT
                tree_template_id,
                tree_template_id || '-' || tree_structure AS tree_template_identifier,
                tree_type_name || '{SEPARATOR}' || key_template_name || '{SEPARATOR}' || tree_template_height || '{SEPARATOR}' || tree_template_keys_amount || '{SEPARATOR}' || tree_template_difficulty AS tree_template_description
            FROM
                tree_template JOIN
                key_template USING (key_template_id) JOIN
                tree_type USING (tree_type_id)
            WHERE
                tree_type_id IN {tree_types_ids} AND
                tree_template_height IN {tree_height} AND
                tree_template_keys_amount BETWEEN {node_count_min} AND {node_count_max} AND
                key_template_id IN {key_templates_ids} AND
                tree_template_difficulty BETWEEN {difficulty_min} AND {difficulty_max} AND
                teacher_id = {teacher_id}
            ORDER BY
                tree_template_id DESC
        ''',
        connection
    )


def get_other_tree_templates(connection: Connection,  
                            teacher_id: int, 
                            tree_height: tuple[int], 
                            node_count_min: int, 
                            node_count_max: int,
                            key_templates_ids: tuple[int], 
                            tree_types_ids: tuple[int], 
                            difficulty_min: float,
                            difficulty_max: float) -> DataFrame:
    '''
        Функция для получения DataFrame, 
        включащего отфильтрованную информацию о шаблонах деревьев, 
        созданных оставльными преподавателями
    '''

    return read_sql(
        f'''
            SELECT
                tree_template_id,
                tree_template_id || '-' || tree_structure AS tree_template_identifier,
                tree_type_name || '{SEPARATOR}' || key_template_name || '{SEPARATOR}' || tree_template_height || '{SEPARATOR}' || tree_template_keys_amount || '{SEPARATOR}' || tree_template_difficulty AS tree_template_description
            FROM
                tree_template JOIN
                key_template USING (key_template_id) JOIN
                tree_type USING (tree_type_id)
            WHERE
                tree_type_id IN {tree_types_ids} AND
                tree_template_height IN {tree_height} AND
                tree_template_keys_amount BETWEEN {node_count_min} AND {node_count_max} AND
                key_template_id IN {key_templates_ids} AND
                tree_template_difficulty BETWEEN {difficulty_min} AND {difficulty_max} AND
                teacher_id <> {teacher_id}
            ORDER BY
                tree_template_id DESC
        ''',
        connection
    )

