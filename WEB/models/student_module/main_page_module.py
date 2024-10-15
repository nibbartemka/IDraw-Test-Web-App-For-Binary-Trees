from __future__ import annotations
from pandas import read_sql
from app import SEPARATOR


def get_upcoming_testing_session(connection: Connection, current_date: date, current_time: datetime, student_id: int) -> DataFrame:

    return read_sql(
        f'''
            SELECT DISTINCT
                testing_session_id,
                testing_session_name || '{SEPARATOR}' || testing_session_date || '{SEPARATOR}' || testing_session_begin_time || '{SEPARATOR}' || testing_session_end_time || '{SEPARATOR}' || test_template_bar AS testing_session_description,
                testing_session_date
            FROM
                testing_session
            JOIN 
                student_testing_session sts USING(testing_session_id),
                test t USING(testing_session_id)
            WHERE
                (testing_session_date > '{current_date}' OR (
                testing_session_date = '{current_date}' AND
                testing_session_end_time >= '{current_time}')) AND
                sts.student_id = '{student_id}' AND (t.test_mark IS NULL) AND t.student_id = '{student_id}'
            ORDER BY
                testing_session_date,
                testing_session_begin_time
        ''',
        connection
    )


def get_passed_testing_session(connection: Connection, current_date: date, current_time: datetime, student_id: int) -> DataFrame:
    return read_sql(
        f'''
            SELECT DISTINCT
                testing_session_id,
                testing_session_name || '{SEPARATOR}' || testing_session_date || '{SEPARATOR}' || testing_session_begin_time || '{SEPARATOR}' || testing_session_end_time || '{SEPARATOR}' || test_template_bar AS testing_session_description,
                testing_session_date,test_mark,test_template_bar
            FROM
                testing_session
            JOIN 
                student_testing_session sts USING(testing_session_id),
                test t USING(testing_session_id)
            WHERE
                ((testing_session_date < '{current_date}' OR (
                testing_session_date = '{current_date}' AND
                testing_session_end_time < '{current_time}')) OR (t.test_mark IS NOT NULL)) AND
                sts.student_id = {student_id} AND
				t.student_id = {student_id}
            ORDER BY
                testing_session_date DESC,
                testing_session_begin_time
        ''',
        connection
    )


def get_all_students(connection: Connection) -> DataFrame:
    return read_sql(
        f'''
            SELECT student_id
            FROM student
        ''',
        connection
    )


def get_all_testing_session(connection: Connection) -> DataFrame:
    return read_sql(
        f'''
            SELECT testing_session_id
            FROM testing_session
        ''',
        connection
    )


def get_all_testing_session_student(connection: Connection) -> DataFrame:
    return read_sql(
        f'''
            SELECT student_id, testing_session_id
            FROM student_testing_session
            ORDER BY student_id
        ''',
        connection
    )


def update_bd_every_minute(connection: Connection, student_id: int, testing_session_id: int) -> DataFrame:
    '''
        Функция для обновления теста
    '''
    cursor = connection.cursor()

    cursor.execute(
        f'''
            INSERT INTO "test" (
            "student_id",
            "testing_session_id"
            )
            SELECT
                {student_id},
                {testing_session_id}
            FROM (
                SELECT 1
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM "test"
                    WHERE 
                    "student_id" = {student_id}
                    AND "testing_session_id" = {testing_session_id}
                )
            ) AS subquery
        '''
    )
    cursor.close()
    connection.commit()
