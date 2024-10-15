from __future__ import annotations
from pandas import read_sql
from app import SEPARATOR


def get_suboperations(connection: Connection, operation_template_id: int) -> DataFrame:
    return read_sql(
        f'''
            SELECT
                suboperation_template_id,
                suboperation_text,
                input_template.is_tree AS input_is_tree,
                output_template.is_tree AS output_is_tree
            FROM
                operation_suboperation_template JOIN
                suboperation_template USING (suboperation_template_id) JOIN
                input_template USING (input_template_id) JOIN
                output_template USING (output_template_id)
            WHERE
                operation_template_id = {operation_template_id}
        ''',
        connection
    )


def get_operation(connection: Connection, operation_template_id: int, task_template_id: int) -> DataFrame:
    return read_sql(
        f'''
            SELECT
                operation_template_id,
                operation_name,
                input_template.is_tree AS input_is_tree,
                output_template.is_tree AS output_is_tree,
                operation_text,
                node_index,
                task_template_id
            FROM
                task_template JOIN
                operation_template USING (operation_template_id) JOIN
                input_template USING (input_template_id) JOIN
                output_template USING (output_template_id)
            WHERE
                operation_template_id = {operation_template_id}
                AND task_template_id = {task_template_id}
        ''',
        connection
    )


def get_task_info(connection: Connection, testing_session_id: int, task_template_id: int) -> DataFrame:
    return read_sql(
        f'''
            SELECT
                DISTINCT 
                    testing_session_id,
                    testing_session_name,
                    task_template_id,
                    operation_template_id,
                    operation_name,
                    tree_template_id,
                    tree_template.tree_type_id,
                    tree_type_name,
                    formula_task_id,
                    formula_task_body,
                    input_template_id,
                    output_template_id,
                    input_template.is_tree AS is_tree_input,
                    output_template.is_tree AS is_tree_output,
                    node_index,
                    key_template_id,
                    key_template_name,
                    tree_structure,
                    tree_template_height
            FROM
                testing_session
            JOIN 
                test_template USING(test_template_id),
                test_task_template USING(test_template_id),
                task_template USING(task_template_id),
                operation_template USING(operation_template_id),
                tree_template USING(tree_template_id),
                tree_type USING(tree_type_id),
                formula_task USING(formula_task_id),
                input_template USING(input_template_id),
                output_template USiNG(output_template_id),
                key_template USING(key_template_id)
            WHERE
                testing_session_id = {testing_session_id}
                and task_template_id = {task_template_id}
        ''',
        connection
    )


def get_test_info(connection: Connection, testing_session_id: int) -> DataFrame:
    return read_sql(
        f'''
            SELECT
                test_template_bar,
                formula_test_body,
                GROUP_CONCAT(task_template_difficulty, ';') AS task_difficulties
            FROM
                testing_session JOIN
                formula_test USING (formula_test_id) JOIN
                test_template USING (test_template_id) JOIN
                test_task_template USING (test_template_id) JOIN
                task_template USING (task_template_id)
            WHERE
                testing_session_id = {testing_session_id}
            GROUP BY
                test_template_id
        ''',
        connection
    )


def get_test_tasks(connection: Connection, testing_session_id: int) -> DataFrame:
    return read_sql(
        f'''
            SELECT 
                testing_session_name,
                task_template_id,
                operation_name,
                tree_template_id,
                tree_type_name
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


def get_tasks_testing_session(connection: Connection, testing_session_id: int) -> DataFrame:

    return read_sql(
        f'''
            SELECT 
                testing_session_name,task_template_id,operation_name,tree_template_id,tree_type_name
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


def get_sub_and_operation(connection: Connection, testing_session_id: int) -> DataFrame:

    return read_sql(
        f'''
            SELECT 
                testing_session_name,task_template_id,operation_name,tree_template_id,tree_type_name
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


def get_test_id(connection: Connection, student_id: int, testing_session_id: int) -> DataFrame:

    return read_sql(
        f'''
            SELECT 
                test_id
            from 
                test
            where 
                student_id={student_id} and testing_session_id = {testing_session_id}
        ''',
        connection
    )


def add_into_task(connection: Connection, task_template_id: int, test_id: int, tree_template_id: int, task_score: int) -> DataFrame:

    cursor = connection.cursor()

    cursor.execute(
        f'''
        INSERT INTO " task" (
        "task_template_id",
        "test_id",
        "tree_template_id",
        "task_score") 

        VALUES (
        {task_template_id},
        {test_id},
        {tree_template_id},
        {task_score}
        );'''
    )
    cursor.close()
    connection.commit()


def add_into_test_end(connection: Connection, test_mark: int, test_date: DATE,  test_time_end: TIME,
                      test_id: int) -> DataFrame:

    cursor = connection.cursor()

    cursor.execute(
        f'''
         UPDATE "test"
            SET
            "test_mark" = {test_mark},
            "test_date" = '{test_date}',
            "test_time_end" = '{test_time_end}'
            WHERE test_id = '{test_id}';
''')

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
