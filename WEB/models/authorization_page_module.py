from __future__ import annotations
from pandas import read_sql
from app import SEPARATOR


def get_student_id(connection: Connection, login: int, password: int) -> DataFrame:
    query = """
        SELECT 
            student_id,student_name
        FROM
            student
        WHERE
            student_login = ? AND
            student_password = ?
    """
    return read_sql(query, connection, params=[login, password])


def get_teacher_id(connection: Connection, login: int, password: int) -> DataFrame:

    query = """
        SELECT 
            teacher_id,teacher_name
        FROM
            teacher
        WHERE
            teacher_login = ? AND
            teacher_password = ?
    """

    return read_sql(query, connection, params=[login, password])


def get_login_password_teacher(connection: Connection, teacher_id: int) -> DataFrame:

    return read_sql(
        f'''
            SELECT DISTINCT
                teacher_login,teacher_password
            FROM
                teacher
            WHERE
                teacher_id = '{teacher_id}'
        ''',
        connection
    )


def set_teacher_name(connection: Connection, teacher_id: int, full_name: int) -> DataFrame:

    cursor = connection.cursor()

    cursor.execute(
        f'''
         UPDATE "teacher"
            SET teacher_name = '{full_name}'
            WHERE teacher_id = '{teacher_id}';
''')

    cursor.close()
    connection.commit()
