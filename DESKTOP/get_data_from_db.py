import sqlite3

# Получение всех СТ
def get_ST():
    ST = []
    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    query = '''SELECT testing_session_name, testing_session_id
                FROM testing_session'''
    cursor.execute(query)

    for name in cursor.fetchall():
        ST.append(f'{name[0]} ({name[1]})')
    
    conn.commit()
    conn.close()

    return ST

# Получение всех ШТ
def get_SHT():
    SHT = []
    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    query = '''SELECT test_template_id 
                FROM test_template'''
    cursor.execute(query)

    for name in cursor.fetchall():
        SHT.append(name[0])
    
    conn.commit()
    conn.close()

    return SHT

# Получение названий групп, которые проходили конкретные СТ
def get_groups_ST(id_ST):
    groups = set()

    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    for ST in id_ST:
        query = '''SELECT DISTINCT group_name
                    FROM testing_session
                    LEFT JOIN test USING (testing_session_id)
                    LEFT JOIN student USING (student_id)
                    LEFT JOIN subgroup USING (subgroup_id)
                    LEFT JOIN student_group USING (group_id)
                    WHERE testing_session_id = :p_id'''
        cursor.execute(query, {'p_id': ST})

        for name in cursor.fetchall():
            groups.add(name[0])

    conn.commit()
    conn.close()

    return sorted(list(groups))

# Получение названий групп, которые проходили конкретные ШТ
def get_groups_SHT(num_SHT):
    groups = set()

    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    for SHT in num_SHT:
        query = '''SELECT DISTINCT group_name
                    FROM testing_session
                    LEFT JOIN test USING (testing_session_id)
                    LEFT JOIN student USING (student_id)
                    LEFT JOIN subgroup USING (subgroup_id)
                    LEFT JOIN student_group USING (group_id)
                    WHERE testing_session.test_template_id = :p_num'''
        cursor.execute(query, {'p_num': SHT})

        for name in cursor.fetchall():
            groups.add(name[0])
    
    conn.commit()
    conn.close()

    return sorted(list(groups))

# Получение годов, в которые проходили конкретные ШТ
def get_years_SHT(num_SHT):
    years = set()

    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    for SHT in num_SHT:
        query = '''SELECT DISTINCT strftime('%Y', testing_session_date)
                    FROM testing_session
                    WHERE test_template_id = :p_num'''
        cursor.execute(query, {'p_num': SHT})

        for year in cursor.fetchall():
            years.add(year[0])
    
    conn.commit()
    conn.close()

    return sorted(list(years))



# Получение оценок у групп по одному СТ
def get_marks_groups_one_ST(id_ST, groups):
    marks = {}

    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    for group in groups:
        query = '''SELECT test_mark, test_template_bar
                    FROM testing_session
                    LEFT JOIN test USING (testing_session_id)
                    LEFT JOIN student USING (student_id)
                    LEFT JOIN subgroup USING (subgroup_id)
                    LEFT JOIN student_group USING (group_id)
                    WHERE testing_session_id = :p_id and group_name = :p_group'''
        cursor.execute(query, {'p_id': id_ST, 'p_group': group})
        
        marks[group] = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return marks

# Получение оценок у групп по одному ШТ
def get_marks_groups_one_SHT(num_SHT, groups):
    marks = {}

    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    for group in groups:
        query = '''SELECT test_mark, test_template_bar
                    FROM testing_session
                    LEFT JOIN test USING (testing_session_id)
                    LEFT JOIN student USING (student_id)
                    LEFT JOIN subgroup USING (subgroup_id)
                    LEFT JOIN student_group USING (group_id)
                    WHERE testing_session.test_template_id = :p_num and group_name = :p_group'''
        cursor.execute(query, {'p_num': num_SHT, 'p_group': group})
        
        marks[group] = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return marks

# Получение оценок у годов по одному ШТ
def get_marks_years_one_SHT(num_SHT, years):
    marks = {}

    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    for year in years:
        query = '''SELECT test_mark, test_template_bar
                    FROM testing_session
                    LEFT JOIN test USING (testing_session_id)
                    LEFT JOIN student USING (student_id)
                    LEFT JOIN subgroup USING (subgroup_id)
                    LEFT JOIN student_group USING (group_id)
                    WHERE testing_session.test_template_id = :p_num and strftime('%Y', testing_session_date) = :p_year'''
        cursor.execute(query, {'p_num': num_SHT, 'p_year': year})
        
        marks[year] = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return marks

# Получение оценок у групп по нескольким СТ
def get_marks_groups_many_ST(id_ST, groups):
    marks = {}

    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    for id in id_ST:
        marks[id] = {}
        for group in groups:
            query = '''SELECT test_mark, test_template_bar
                        FROM testing_session
                        LEFT JOIN test USING (testing_session_id)
                        LEFT JOIN student USING (student_id)
                        LEFT JOIN subgroup USING (subgroup_id)
                        LEFT JOIN student_group USING (group_id)
                        WHERE testing_session_id = :p_id and group_name = :p_group'''
            cursor.execute(query, {'p_id': id, 'p_group': group})
            
            marks[id][group] = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return marks

# Получение оценок у групп по нескольким ШТ
def get_marks_groups_many_SHT(num_SHT, groups):
    marks = {}

    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    for num in num_SHT:
        marks[num] = {}
        for group in groups:
            query = '''SELECT test_mark, test_template_bar
                        FROM testing_session
                        LEFT JOIN test USING (testing_session_id)
                        LEFT JOIN student USING (student_id)
                        LEFT JOIN subgroup USING (subgroup_id)
                        LEFT JOIN student_group USING (group_id)
                        WHERE testing_session.test_template_id = :p_num and group_name = :p_group'''
            cursor.execute(query, {'p_num': num, 'p_group': group})
            
            marks[num][group] = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return marks

# Получение оценок у годов по нескольким ШТ
def get_marks_years_many_SHT(num_SHT, years):
    marks = {}

    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    for num in num_SHT:
        marks[num] = {}
        for year in years:
            query = '''SELECT test_mark, test_template_bar
                        FROM testing_session
                        LEFT JOIN test USING (testing_session_id)
                        LEFT JOIN student USING (student_id)
                        LEFT JOIN subgroup USING (subgroup_id)
                        LEFT JOIN student_group USING (group_id)
                        WHERE testing_session.test_template_id = :p_num and strftime('%Y', testing_session_date) = :p_year'''
            cursor.execute(query, {'p_num': num, 'p_year': year})
            
            marks[num][year] = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return marks


# Получение оценок за ШТЗ в СТ (анализ качества)
def get_marks_ST(id_ST):
    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    query = '''SELECT student_id, task_score, task_template_id, task_template_difficulty
                FROM testing_session
                LEFT JOIN test USING (testing_session_id)
                LEFT JOIN ' task' USING (test_id)
                LEFT JOIN student USING (student_id)
                LEFT JOIN task_template USING (task_template_id)
                WHERE testing_session_id = :p_id
                ORDER BY student_id, task_template_id'''
    cursor.execute(query, {'p_id': id_ST})

    marks = cursor.fetchall()
    print(marks)
    
    conn.commit()
    conn.close()

    return marks

# Получение данных студентов по их id (анализ качества)
def get_stud(id_stud):
    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    query = '''SELECT student_name, group_name, subgroup_num
                FROM student
                LEFT JOIN subgroup USING (subgroup_id)
                LEFT JOIN student_group USING (group_id)
                WHERE student_id = :p_id'''
    cursor.execute(query, {'p_id': id_stud})

    stud = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return stud

# Получение оценок за ШТЗ в ШТ (анализ качества)
def get_marks_SHT(id_SHT):
    conn = sqlite3.connect('idraw.sqlite')
    cursor = conn.cursor()

    query = '''SELECT student_id, task_score, task_template_id
                FROM testing_session
                LEFT JOIN test USING (testing_session_id)
                LEFT JOIN ' task' USING (test_id)
                LEFT JOIN student USING (student_id)
                WHERE testing_session_id = (
                    SELECT testing_session_id
                    FROM testing_session
                    WHERE testing_session.test_template_id = :p_id
                    ORDER BY testing_session_date DESC, testing_session_begin_time DESC, testing_session_end_time DESC, testing_session_id
                    LIMIT 1
                )'''
    cursor.execute(query, {'p_id': id_SHT})

    marks = cursor.fetchall()
    
    conn.commit()
    conn.close()

    return marks