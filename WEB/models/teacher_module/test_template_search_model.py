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



def get_operation_template(connection: Connection) -> tuple[int]:
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


def get_my_test_templates(connection: Connection,  
                            teacher_id: int, 
                            key_templates_ids: tuple[int], 
                            tree_types_ids: tuple[int],
                            operation_template: tuple[str],
                            difficulty_min: float,
                            difficulty_max: float,
                            task_count_min: int,
                            task_count_max: int,
                            ) -> DataFrame:
    '''
        Функция для получения DataFrame, 
        включащего отфильтрованную информацию о шаблонах тестов, 
        созданных определенным преподавателем
    '''

    return read_sql(
        f'''
            WITH get_test_keys
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    test_task_template USING (test_template_id) JOIN
                    task_template USING (task_template_id) JOIN
                    tree_template USING (tree_template_id) JOIN
                    key_template USING (key_template_id)
                WHERE
                    key_template_id IN {key_templates_ids}
                GROUP BY
                    test_template_id
            ),
            get_test_tree_types
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    test_task_template USING (test_template_id) JOIN
                    task_template USING (task_template_id) JOIN
                    tree_template USING (tree_template_id) JOIN
                    tree_type USING (tree_type_id)
                WHERE
                    tree_type_id IN {tree_types_ids}
                GROUP BY
                    test_template_id
            ),
            get_test_operations
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    test_task_template USING (test_template_id) JOIN
                    task_template USING (task_template_id) JOIN
                    operation_template USING (operation_template_id)
                WHERE
                    operation_name IN {operation_template}
                GROUP BY
                    test_template_id
            ),
            get_test_task_count
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    test_task_template USING (test_template_id) 
                GROUP BY
                    test_template_id
                HAVING
                    COUNT(task_template_id) BETWEEN {task_count_min} AND {task_count_max}
            ),
            get_test_difficulty
            AS (
                SELECT
                    test_template_id,
                    test_template_difficulty
                FROM
                    test_template
                WHERE
                    test_template_difficulty BETWEEN {difficulty_min} AND {difficulty_max}
            ),
            get_test_template_id
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    get_test_keys USING (test_template_id) JOIN
                    get_test_tree_types USING (test_template_id) JOIN
                    get_test_operations USING (test_template_id) JOIN
                    get_test_task_count USING (test_template_id) JOIN
                    get_test_difficulty USING (test_template_id)
                WHERE
                    teacher_id = {teacher_id}
            )

            SELECT
                test_template_id,
                test_template_difficulty,
                COUNT(DISTINCT task_template_id) AS distinct_task_count,
                COUNT(task_template_id) AS task_count       
            FROM
                test_template JOIN
                test_task_template USING (test_template_id)
            WHERE
                test_template_id IN (SELECT test_template_id FROM get_test_template_id)
            GROUP BY
                test_template_id
        ''',
        connection
    )


def get_test_tasks(connection: Connection, test_template_id: int) -> DataFrame:
    return read_sql(
        f'''
            SELECT
                COUNT(task_template_id) AS task_count,
                operation_name || '{SEPARATOR}' || tree_type_name || '{SEPARATOR}' || key_template_name || '{SEPARATOR}' || tree_template_height || '{SEPARATOR}' || tree_template_keys_amount AS task_template_description
            FROM
                test_task_template JOIN
                task_template USING (task_template_id) JOIN 
                tree_template USING (tree_template_id) JOIN
                key_template USING (key_template_id) JOIN
                tree_type USING (tree_type_id) JOIN
                operation_template USING (operation_template_id)
            WHERE
                test_template_id = {test_template_id}
            GROUP BY
                task_template_id
        ''',
        connection
    )


def get_other_test_templates(connection: Connection,  
                            teacher_id: int, 
                            key_templates_ids: tuple[int], 
                            tree_types_ids: tuple[int],
                            operation_template: tuple[str],
                            difficulty_min: float,
                            difficulty_max: float,
                            task_count_min: int,
                            task_count_max: int,
                            ) -> DataFrame:
    '''
        Функция для получения DataFrame, 
        включащего отфильтрованную информацию о шаблонах тестов, 
        созданных определенным преподавателем
    '''

    return read_sql(
        f'''
            WITH get_test_keys
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    test_task_template USING (test_template_id) JOIN
                    task_template USING (task_template_id) JOIN
                    tree_template USING (tree_template_id) JOIN
                    key_template USING (key_template_id)
                WHERE
                    key_template_id IN {key_templates_ids}
                GROUP BY
                    test_template_id
            ),
            get_test_tree_types
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    test_task_template USING (test_template_id) JOIN
                    task_template USING (task_template_id) JOIN
                    tree_template USING (tree_template_id) JOIN
                    tree_type USING (tree_type_id)
                WHERE
                    tree_type_id IN {tree_types_ids}
                GROUP BY
                    test_template_id
            ),
            get_test_operations
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    test_task_template USING (test_template_id) JOIN
                    task_template USING (task_template_id) JOIN
                    operation_template USING (operation_template_id)
                WHERE
                    operation_name IN {operation_template}
                GROUP BY
                    test_template_id
            ),
            get_test_task_count
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    test_task_template USING (test_template_id) 
                GROUP BY
                    test_template_id
                HAVING
                    COUNT(task_template_id) BETWEEN {task_count_min} AND {task_count_max}
            ),
            get_test_difficulty
            AS (
                SELECT
                    test_template_id,
                    test_template_difficulty
                FROM
                    test_template
                WHERE
                    test_template_difficulty BETWEEN {difficulty_min} AND {difficulty_max}
            ),
            get_test_template_id
            AS (
                SELECT
                    test_template_id
                FROM
                    test_template JOIN
                    get_test_keys USING (test_template_id) JOIN
                    get_test_tree_types USING (test_template_id) JOIN
                    get_test_operations USING (test_template_id) JOIN
                    get_test_task_count USING (test_template_id) JOIN
                    get_test_difficulty USING (test_template_id)
                WHERE
                    teacher_id <> {teacher_id}
            )

            SELECT
                test_template_id,
                test_template_difficulty,
                COUNT(DISTINCT task_template_id) AS distinct_task_count,
                COUNT(task_template_id) AS task_count       
            FROM
                test_template JOIN
                test_task_template USING (test_template_id)
            WHERE
                test_template_id IN (SELECT test_template_id FROM get_test_template_id)
            GROUP BY
                test_template_id
        ''',
        connection
    )

