from __future__ import annotations
from pandas import read_sql
from app import SEPARATOR


def is_testing_session_passed(connection: Connection, testing_session_id) -> bool:
    cursor = connection.cursor()
    cursor.execute(
        f'''
            SELECT
                test_id
            FROM
                test
            WHERE
                EXISTS(
                    SELECT 1
                    FROM test
                    WHERE testing_session_id = {testing_session_id} AND
                    test_mark is not null
                )
                
        '''
    )

    return bool(cursor.fetchall())


def get_test_template_data(connection: Connection, test_template_id) -> dict[str, Any] | None:
    '''
        Функция для получения словаря, хранящего данные о шаблоне теста
    '''

    data = read_sql(
        f'''
            SELECT
                test_template_id,
                'Типы деревьев: ' || GROUP_CONCAT(DISTINCT tree_type_name) || '{SEPARATOR}Операции: ' || GROUP_CONCAT(DISTINCT operation_name) || '{SEPARATOR}Типы ключей: ' || GROUP_CONCAT(DISTINCT key_template_name) || '{SEPARATOR}Общее кол-во заданий: ' ||  COUNT(task_template_id) || '{SEPARATOR}Сложность: ' || test_template_difficulty AS test_template_description       
            FROM
                test_template JOIN
                test_task_template USING (test_template_id) JOIN
                task_template USING (task_template_id) JOIN
                tree_template USING (tree_template_id) JOIN
                key_template USING (key_template_id) JOIN
                tree_type USING (tree_type_id) JOIN
                operation_template USING (operation_template_id)
            WHERE
                test_template_id = {test_template_id}
            GROUP BY
                test_template_id
        ''',
        connection
    ).to_dict('records')

    return data[0] if data else None


def get_subgroup_data(connection: Connection, subgroup_ids: tuple[int]) -> list[dict[str, Any]]:
    '''
        Функция для получения словаря, хранящего данные о подгруппах
    '''

    if not subgroup_ids:
        return ()

    data = read_sql(
        f'''
            SELECT
                subgroup_id,
                group_name || group_majority || '(' || subgroup_num || ')' AS subgroup_identifier,
                'Кол-во студентов: ' || COUNT(student_id) AS student_count
            FROM
                subgroup JOIN
                student_group USING (group_id) LEFT JOIN
                student USING (subgroup_id)
            WHERE
                subgroup_id IN {(*subgroup_ids, subgroup_ids[0])}   
            GROUP BY
                subgroup_id
        ''',
        connection
    ).to_dict('records')

    return data


def get_formulas(connection: Connection) -> DataFrame:
    '''
        Функция для получения Dataframe с информацией о формулах теста
    '''

    return read_sql(
        f'''
            SELECT
                *
            FROM
                formula_test
        ''',
        connection
    )


def add_testing_session(
    connection: Connection,
    test_template_id: int,
    testing_session_name: str,
    testing_session_date: str,
    testing_session_begin_time: str,
    testing_session_end_time: str,
    testing_session_bar: int,
    formula_test_id: int,
    teacher_id: int
) -> int:

    cursor = connection.cursor()
    cursor.execute(
        f'''
            INSERT INTO testing_session (
                test_template_id, 
                testing_session_name,
                testing_session_date, 
                testing_session_begin_time, 
                testing_session_end_time, 
                test_template_bar, 
                formula_test_id,
                teacher_id
            )
            VALUES
                (
                    {test_template_id},
                    '{testing_session_name}',
                    '{testing_session_date}',
                    '{testing_session_begin_time}',
                    '{testing_session_end_time}',
                    {testing_session_bar},
                    {formula_test_id},
                    {teacher_id}
                )
        '''
    )
    connection.commit()

    return cursor.lastrowid


def add_student_testing_session(connection: Connection, testing_session_id: int, subgroup_ids: tuple[int]) -> None:
    connection.executescript(
        f'''
            INSERT INTO student_testing_session (student_id, testing_session_id)
            SELECT 
                student_id, 
                {testing_session_id} 
            FROM 
                student 
            WHERE 
                subgroup_id IN {subgroup_ids} AND
                subgroup_id NOT IN (
                    SELECT
                        subgroup_id
                    FROM
                        student_testing_session JOIN
                        student USING (student_id)
                    WHERE
                        testing_session_id = {testing_session_id}
                );
        '''
    )
    connection.commit()
    connection.execute(
        f'''    
            INSERT INTO test (student_id, testing_session_id, test_mark)
            SELECT
                student_id,
                {testing_session_id},
                NULL
            FROM
                student JOIN
                student_testing_session USING (student_id)
            WHERE
                testing_session_id = {testing_session_id} AND
                student_id NOT IN (
                    SELECT
                        student_id
                    FROM
                        test
                    WHERE
                        testing_session_id = {testing_session_id}
                )
        '''
    )
    connection.commit()


def get_testing_session(connection: Connection, testing_session_id: int) -> dict[str, Any]:
    data = read_sql(
        f'''
            SELECT
                teacher_id,
                test_template_id,
                testing_session_name,
                testing_session_date,
                testing_session_begin_time,
                testing_session_end_time,
                test_template_bar,
                formula_test_id,
                REPLACE(GROUP_CONCAT(DISTINCT subgroup_id), ',', '{SEPARATOR}') AS subgroup_ids
            FROM
                testing_session LEFT JOIN
                student_testing_session USING (testing_session_id) LEFT JOIN
                student USING (student_id)
            WHERE
                testing_session_id = {testing_session_id}
            GROUP BY
                teacher_id,
                test_template_id,
                testing_session_name,
                testing_session_date,
                testing_session_begin_time,
                testing_session_end_time,
                test_template_bar,
                formula_test_id
        ''',
        connection
    )

    return data.to_dict('records')[0]


def delete_testing_session(connection: Connection, testing_session_id: int) -> None:
    connection.executescript(
        f'''
            DELETE FROM testing_session
            WHERE testing_session_id = {testing_session_id};

            DELETE FROM student_testing_session
            WHERE testing_session_id = {testing_session_id};
        '''
    )

    connection.commit()


def update_testing_session(
        connection: Connection,
        testing_session_id: int,
        test_template_id: int,
        testing_session_name: str,
        testing_session_date: str,
        testing_session_begin_time: str,
        testing_session_end_time: str,
        testing_session_bar: int,
        formula_test_id: int,
) -> None:

    connection.execute(
        f'''
            UPDATE testing_session
            SET
                test_template_id = {test_template_id},
                testing_session_name = '{testing_session_name}',
                testing_session_date = '{testing_session_date}',
                testing_session_begin_time = '{testing_session_begin_time}',
                testing_session_end_time = '{testing_session_end_time}',
                test_template_bar = {testing_session_bar},
                formula_test_id = {formula_test_id}
            WHERE
                testing_session_id = {testing_session_id}
        '''
    )
    connection.commit()


def delete_student_testing_session(connection: Connection, testing_session_id: int, subgroup_ids: tuple[int]) -> None:
    connection.execute(
        f'''
            DELETE FROM student_testing_session
            WHERE testing_session_id IN (
                SELECT
                    testing_session_id
                FROM
                    student_testing_session JOIN
                    student USING (student_id)
                WHERE
                    testing_session_id = {testing_session_id} AND 
                    subgroup_id NOT IN {subgroup_ids}
            )
        '''
    )
    connection.commit()
