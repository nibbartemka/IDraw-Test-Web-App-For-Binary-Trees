from __future__ import annotations
from pandas import read_sql


def update_difficulty(connection: Connection, test_template_id: int, test_template_difficulty: float) -> None:
    '''
        Функция обновления сложности шаблона теста
    '''
    connection.execute(
        f'''
            UPDATE test_template
            SET test_template_difficulty = {test_template_difficulty}
            WHERE test_template_id = {test_template_id}
        '''
    )
    connection.commit()


def get_test_teacher_id(connection: Connection, test_template_id: int) -> int:
    '''
        Функция позволяет получить teacher_id шаблона теста
    '''

    cursor = connection.cursor()
    cursor.execute(
        f'''
            SELECT
                teacher_id
            FROM
                test_template
            WHERE   
                test_template_id = {test_template_id}
        '''
    )
    
    return cursor.fetchone()[0]    


def check_test_template_include(connection: Connection, test_template_id: int) -> bool:
    '''
        Функция позволяет проверить включен ли шаблонный тест хотя бы один сеанс тестирования
    '''
    cursor = connection.cursor()
    cursor.execute(
        f'''
            SELECT
                testing_session_id
            FROM
                testing_session
            WHERE
                test_template_id = {test_template_id};
        '''
    )

    return bool(cursor.fetchone())


def del_test_task_templates(connection: Connection, test_template_id: int) -> None:
    '''
        Функция для удаления шаблонов тестовых заданий шаблонного теста
    '''
    connection.execute(
        f'''
            DELETE FROM
                test_task_template
            WHERE
                test_template_id = {test_template_id};
        '''
    )
    connection.commit()
    

def del_test_template(connection: Connection, test_template_id: int) -> None:
    '''
        Функция для удаления шаблона теста
    '''
    connection.executescript(
        f'''
            DELETE FROM
                test_template
            WHERE
                test_template_id = {test_template_id};

            DELETE FROM
                test_task_template
            WHERE
                test_template_id = {test_template_id};
        '''
    )
    connection.commit()


def get_test_difficulty(connection: Connection, test_template_id: int) -> float:
    '''
        функция для получения значения сложности шаблона теста
    '''

    cursor = connection.cursor()
    cursor.execute(
        f'''
            SELECT
                test_template_difficulty
            FROM
                test_template
            WHERE   
                test_template_id = {test_template_id}
        '''
    )
    return cursor.fetchone()[0]


def get_test_template_data(connection: Connection, test_template_id: int) -> dict[int, int]:
    '''
       Функция для получения словаря, содержащего информацию о тестовых заданиях и их количестве 
    '''

    cursor = connection.cursor()
    cursor.execute(
        f'''
            SELECT
                task_template_id,
                COUNT(task_template_id)
            FROM
                test_task_template
            WHERE
                test_template_id = {test_template_id}
            GROUP BY
                test_template_id,
                task_template_id
        '''
    )
    return {
        key: value
        for key, value in cursor.fetchall()
    }

def get_task_template_data(connection: Connection, task_template_ids: tuple[int]) -> DataFrame:
    '''
        Функция для получения Dataframe информации о шаблонах тестовых заданий
    '''
    
    return read_sql(
        f'''
            SELECT
                task_template_id,
                task_template_id || '-' || tree_structure AS task_template_identifier,
                operation_name || ', ' || tree_type_name || ', ' || key_template_name || ' ключ, ' || 'высота ' || tree_template_height || ', ключей ' || tree_template_keys_amount || ', сложность ' || task_template_difficulty AS task_template_description
            FROM
                task_template JOIN
                tree_template USING (tree_template_id) JOIN
                key_template USING (key_template_id) JOIN
                tree_type USING (tree_type_id) JOIN
                operation_template USING (operation_template_id)
            WHERE
                task_template_id IN {task_template_ids}
        ''',
        connection
    )


def add_test_template(connection: Connection, difficulty: float, teacher_id: int) -> int:
    '''
        Функция для добавления шаблона теста
    '''

    cursor = connection.cursor()
    cursor.execute(
        f'''
            INSERT INTO test_template (test_template_difficulty, teacher_id)
            VALUES
                ({difficulty}, {teacher_id})
        '''
    )
    connection.commit()
    
    return cursor.lastrowid


def add_task_to_test_template(connection: Connection, test_template_id: int, task_template_id: int) -> None:
    '''
        Функция для добавления шаблона тестового задания для шаблона теста
    '''

    cursor = connection.cursor()
    cursor.execute(
        f'''
            INSERT INTO test_task_template (test_template_id, task_template_id)
            VALUES
                ({test_template_id}, {task_template_id})
        '''
    )
    connection.commit()