from __future__ import annotations
from pandas import read_sql
from app import SEPARATOR


def get_login_password(connection: Connection, student_id: int) -> DataFrame:

    return read_sql(
        f'''
            SELECT DISTINCT
                student_login,student_password,student_avatar
            FROM
                student
            WHERE
                student_id = '{student_id}'
        ''',
        connection
    )

def set_student_name(connection: Connection, student_id: int, full_name: int) -> DataFrame:

    cursor = connection.cursor()

    cursor.execute(
        f'''
         UPDATE "student"
            SET student_name = '{full_name}'
            WHERE student_id = '{student_id}';
''')

    cursor.close()
    connection.commit()