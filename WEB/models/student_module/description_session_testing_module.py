from __future__ import annotations
from pandas import read_sql
from app import SEPARATOR


def get_discription_testing_session(connection: Connection, testing_session_id: int) -> DataFrame:

    return read_sql(
        f'''
           	SELECT 
                testing_session_name,teacher_name,testing_session_date,testing_session_begin_time,testing_session_end_time,test_template_bar,
                COUNT(testing_session_name) as count_task
            FROM 
                testing_session
            JOIN 
                test_template USING(test_template_id),
                test_task_template USING(test_template_id),
				teacher USING(teacher_id)
                
            WHERE
                testing_session_id = {testing_session_id}
            GROUP BY
                testing_session_id
        ''',
        connection
    )


def get_tasks_testing_session(connection: Connection, testing_session_id: int) -> DataFrame:

    return read_sql(
        f'''
            SELECT 
                testing_session_name,operation_name,tree_type_name
            FROM 
                testing_session
            JOIN 
                test_template USING(test_template_id),
                test_task_template USING(test_template_id),
                task_template USING(task_template_id),
                operation_template USING(operation_template_id),
                tree_template USING(tree_template_id),
                tree_type USING(tree_type_id)
            WHERE
                testing_session_id = {testing_session_id}
        ''',
        connection
    )


def add_into_test_begin(connection: Connection, student_id: int, testing_session_id: int) -> DataFrame:
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


def update_into_test_begin(connection: Connection,  test_time_begin: TIME, student_id: int, testing_session_id: int) -> DataFrame:

    cursor = connection.cursor()

    cursor.execute(
        f'''
         UPDATE "test"
            SET
            "test_time_begin" = '{test_time_begin}'
            WHERE "student_id" = {student_id} AND "testing_session_id" = {testing_session_id};

''')

    cursor.close()
    connection.commit()
