from __future__ import annotations
from pandas import read_sql


def get_my_subgroups(connection: Connection, teacher_id: int, group_id: tuple[int]) -> DataFrame:
    '''
        Функция для получения списка подгрупп преподавателя
    '''

    return read_sql(
        f'''
            SELECT
                subgroup_id,
                group_name || group_majority || '(' || subgroup_num || ')' AS subgroup_identifier,
                COUNT(student_id) AS student_count
            FROM
                subgroup JOIN
                student_group USING (group_id) LEFT JOIN
                student USING (subgroup_id)
            WHERE
                teacher_id = {teacher_id} AND
                group_id IN {group_id}
            GROUP BY
                subgroup_id
        ''',
        connection
    )


def get_other_subgroups(connection: Connection, teacher_id: int, group_id: tuple[int]) -> DataFrame:
    '''
        Функция для получения списка подгрупп, у который данный преподаватель не проводит занятия
    '''

    return read_sql(
        f'''
            SELECT
                subgroup_id,
                group_name || group_majority || '(' || subgroup_num || ')' AS subgroup_identifier,
                COUNT(student_id) AS student_count
            FROM
                subgroup JOIN
                student_group USING (group_id) LEFT JOIN
                student USING (subgroup_id)
            WHERE
                teacher_id <> {teacher_id} AND
                group_id IN {group_id}
            GROUP BY
                subgroup_id
        ''',
        connection
    )


def get_groups(connection: Connection) -> DataFrame:
    return read_sql(
        f'''
            SELECT
                group_id,
                group_name || group_majority AS full_group_name
            FROM
                student_group
        ''',
        connection
    )