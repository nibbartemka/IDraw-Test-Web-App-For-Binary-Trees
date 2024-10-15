from __future__ import annotations
from pandas import read_sql
from app import SEPARATOR


def get_testing_session_subgroups(connection: Connection, testing_session_id: int) -> DataFrame:
    return read_sql(
        f'''
            SELECT
                subgroup_id,
                group_name || group_majority || '(' || subgroup_num || ')' AS subgroup_name
            FROM
                student_testing_session JOIN
                student USING (student_id) JOIN
                subgroup USING (subgroup_id) JOIN
                student_group USING (group_id)
            WHERE
                testing_session_id = {testing_session_id}
            GROUP BY
                subgroup_id
        ''',
        connection
    )


def get_testing_session_completition_data(connection: Connection, testing_session_id: int, subgroup_ids: tuple[int]) -> DataFrame:
    return read_sql(
        f'''
            WITH get_student_test_mark(student_id, test_mark, test_template_bar)
            AS (
                SELECT
                    student_id,
                    test_mark,
                    test_template_bar
                FROM
                    test JOIN
                    testing_session USING (testing_session_id)
                WHERE
                    testing_session_id = {testing_session_id}
            )
            SELECT
                student_name,
                group_name || group_majority || '(' || subgroup_num || ')' AS subgroup_name,
                IFNULL(test_mark || ' из ' || test_template_bar, 'Не выполнил(-а)') AS test_mark
            FROM
                student_testing_session LEFT JOIN
                get_student_test_mark USING (student_id) LEFT JOIN
                student USING (student_id) LEFT JOIN
                subgroup USING (subgroup_id) LEFT JOIN
                student_group USING (group_id)
            WHERE
                testing_session_id = {testing_session_id} AND 
                subgroup_id IN {subgroup_ids}
            ORDER BY
                student_name
        ''',
        connection
    )


def get_upcoming_testing_session(connection: Connection, current_date: date, current_time: datetime, teacher_id: int) -> DataFrame:
    return read_sql(
        f'''
            WITH get_testing_session_student_count(testing_session_id, student_count)
            AS (
                SELECT
                    testing_session_id,
                    COUNT(student_id)
                FROM
                    student_testing_session
                GROUP BY
                    testing_session_id
            ),
            get_testing_session_student_completed_count(testing_session_id, student_completed_count)
            AS (
                SELECT
                    testing_session_id,
                    COUNT(DISTINCT test.student_id)
                FROM
                    student_testing_session LEFT JOIN
                    test USING (testing_session_id)
                WHERE
                    test_mark IS NOT NULL
                GROUP BY
                    testing_session_id  
            )
        
            SELECT
                testing_session_id,
                testing_session_name || '{SEPARATOR}' || testing_session_date || '{SEPARATOR}' || testing_session_begin_time || '{SEPARATOR}' || testing_session_end_time || '{SEPARATOR}' || test_template_bar AS testing_session_description,
                testing_session_date,
                student_count,
                IFNULL(student_completed_count, 0) AS student_completed_count
            FROM
                testing_session LEFT JOIN
                get_testing_session_student_count USING (testing_session_id) LEFT JOIN
                get_testing_session_student_completed_count USING (testing_session_id)
            WHERE
                testing_session_date > '{current_date}' OR (
                testing_session_date = '{current_date}' AND
                testing_session_end_time >= '{current_time}') AND
                teacher_id = {teacher_id}
            ORDER BY
                testing_session_date,
                testing_session_begin_time
        ''',
        connection
    )


def get_passed_testing_session(connection: Connection, current_date: date, current_time: datetime, teacher_id: int) -> DataFrame:
    return read_sql(
        f'''
            WITH get_testing_session_student_count(testing_session_id, student_count)
            AS (
                SELECT
                    testing_session_id,
                    COUNT(student_id)
                FROM
                    student_testing_session
                GROUP BY
                    testing_session_id
            ),
            get_testing_session_student_completed_count(testing_session_id, student_completed_count)
            AS (
                SELECT
                    testing_session_id,
                    COUNT(DISTINCT test.student_id)
                FROM
                    student_testing_session LEFT JOIN
                    test USING (testing_session_id)
                WHERE
                    test_mark IS NOT NULL
                GROUP BY
                    testing_session_id  
            )
            
            SELECT
                testing_session_id,
                testing_session_name || '{SEPARATOR}' || testing_session_date || '{SEPARATOR}' || testing_session_begin_time || '{SEPARATOR}' || testing_session_end_time || '{SEPARATOR}' || test_template_bar AS testing_session_description,
                testing_session_date,
                student_count,
                IFNULL(student_completed_count, 0) AS student_completed_count
            FROM
                testing_session LEFT JOIN
                get_testing_session_student_count USING (testing_session_id) LEFT JOIN
                get_testing_session_student_completed_count USING (testing_session_id)
            WHERE
                testing_session_date < '{current_date}' OR (
                testing_session_date = '{current_date}' AND
                testing_session_end_time < '{current_time}') AND
                teacher_id = {teacher_id}
        ''',
        connection
    )
