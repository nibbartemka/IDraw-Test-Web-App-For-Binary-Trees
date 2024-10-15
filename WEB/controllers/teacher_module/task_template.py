from app import app, DATABASE_NAME
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection, formula_task
from models.teacher_module.task_template_model import *


def transform_num_data(func, data):
    res = None

    try:
        res = float(data)
        res = func(res)
    except Exception:
        pass

    return res


@app.route('/Шаблон-тестового-задания/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Шаблон-тестового-задания/<int:is_directly>', methods=['GET', 'POST'])
def task_template(is_directly):
    connection = get_db_connection(DATABASE_NAME)

    ##################################
    if not session['teacher_id']:
        session['teacher_id'] = 1
    ##################################

    session['task_url'] = request.url
    teacher_id = session['teacher_id']

    tree_type_id = 0
    operation_template_id = 0
    formula_task_id = 1

    session['tree_template_id'] = 0

    url_template_tree = ''
    tree_template_data = ''

    key_template_id = ''
    tree_template_height = ''
    tree_template_keys_amount = ''
    tree_structure = ''

    if request.method == 'GET':
        if request.values.get('tree_template_id'):
            session['tree_template_id'] = int(
                request.values.get('tree_template_id'))
            url_template_tree = url_for(
                'tree_template_edit', tree_template_id=session['tree_template_id'], is_directly=0)
            tree_template_all_data = get_tree_template_data(
                connection, session['tree_template_id']).to_dict('records')[0]
            tree_template_data = f'''
                {tree_template_all_data['tree_type_name']}, {tree_template_all_data['key_template_name']} ключ, 
                высота {tree_template_all_data['tree_template_height']}, ключей {tree_template_all_data['tree_template_keys_amount']}, 
                сложность {tree_template_all_data['tree_template_difficulty']}
            '''
            tree_type_id = tree_template_all_data['tree_type_id']
            key_template_id = tree_template_all_data['key_template_id']
            tree_template_height = tree_template_all_data['tree_template_height']
            tree_template_keys_amount = tree_template_all_data['tree_template_keys_amount']
            tree_structure = tree_template_all_data['tree_structure']
    elif request.method == 'POST':
        if request.values.get('tree_template_id'):
            session['tree_template_id'] = int(
                request.values.get('tree_template_id'))
            try:
                tree_template_all_data = get_tree_template_data(
                    connection, session['tree_template_id']).to_dict('records')[0]
                url_template_tree = url_for(
                    'tree_template_edit', tree_template_id=session['tree_template_id'], is_directly=0)
                tree_template_data = f'''
                    {tree_template_all_data['tree_type_name']}, {tree_template_all_data['key_template_name']} ключ, 
                    высота {tree_template_all_data['tree_template_height']}, ключей {tree_template_all_data['tree_template_keys_amount']}, 
                    сложность {tree_template_all_data['tree_template_difficulty']}
                '''
                tree_type_id = tree_template_all_data['tree_type_id']
                key_template_id = tree_template_all_data['key_template_id']
                tree_template_height = tree_template_all_data['tree_template_height']
                tree_template_keys_amount = tree_template_all_data['tree_template_keys_amount']
                tree_structure = tree_template_all_data['tree_structure']
            except:
                pass
        if 'save_template' in request.form:
            difficulties = {
                key: value
                for key, value in request.form.items()
                if key.startswith("task_template_difficulty")
            }
            node_indexes = {
                key: value
                for key, value in request.form.items()
                if key.startswith("node_index")
            }
            session['tree_template_id'] = int(
                request.values.get('tree_template_id'))
            operation_template_id = request.form.get('operation_template_id')
            formula_task_id = int(request.form.get('formula_task_id'))

            difficulties = list(difficulties.items())
            node_indexes = list(node_indexes.items())

            for index, difficulty in enumerate(difficulties):
                task_template_difficulty = difficulty[1]
                node_index = node_indexes[index][1]

                data_tuple = (session['tree_template_id'], formula_task_id,
                              operation_template_id, task_template_difficulty)
                func_tuple = (int, int, int, float)

                handled_data = [
                    transform_num_data(func, data)
                    for func, data in zip(func_tuple, data_tuple)
                ]

                if all(handled_data):
                    handled_data.append(node_index)
                    handled_data.append(teacher_id)
                    task_template_id = add_task_template(
                        connection, handled_data)

                    if task_template_id:
                        flash(
                            f"Шаблон успешно создан! <a href={url_for('task_template_edit', task_template_id=task_template_id, is_directly=is_directly)}>Перейти к шаблону</a>")
                    else:
                        flash("Шаблон с такими параметрами уже есть в системе!")
                else:
                    flash("Введите все необходимые данные!")
            if not int(request.values.get('tree_template_id')):
                flash("Введите все необходимые данные!")

    df_operations = get_operations(connection, tree_type_id)
    operation_indexes = tuple(df_operations['operation_template_id'])
    operation_values = tuple(df_operations['operation_name'])

    df_formulas = get_formulas(connection)
    formula_indexes = tuple(df_formulas['formula_task_id'])
    formula_pictures = tuple(
        formula_task[formula_id]['picture'] for formula_id in formula_task)

    html = render_template(
        'teacher_module/task_template.html',
        operation_indexes=operation_indexes,
        operation_values=operation_values,
        zip=zip,
        str=str,
        operation_template_id=operation_template_id,
        url_template_tree=url_template_tree,
        tree_template_data=tree_template_data,
        tree_template_id=session['tree_template_id'],
        formula_indexes=formula_indexes,
        formula_pictures=formula_pictures,
        formula_task_id=formula_task_id,
        tree_type_id=tree_type_id,
        key_template_id=key_template_id,
        tree_template_height=tree_template_height,
        tree_template_keys_amount=tree_template_keys_amount,
        test_url=session.get('test_url'),
        is_directly=is_directly,
        tree_structure=tree_structure,
        user_name=session['user_name'],
    )

    return html


@app.route('/Шаблон-тестового-задания/<int:task_template_id>/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Шаблон-тестового-задания/<int:task_template_id>/<int:is_directly>', methods=['GET', 'POST'])
def task_template_edit(task_template_id, is_directly):
    connection = get_db_connection(DATABASE_NAME)
    session['task_url'] = request.url

    task_template = get_task_template(connection, task_template_id).loc[0]

    disable_data = check_task_template_include(
        connection, task_template['task_template_id'])

    ##########################################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    ##########################################

    teacher_id = session['teacher_id']
    disable_data = [
        'tree_template_id',
        'operation_template_id',
        'formula_task_id',
        'task_template_difficulty'
    ] if (task_template['teacher_id'] != teacher_id) else disable_data

    task_template_difficulty = float(task_template['task_template_difficulty'])
    operation_template_id = int(task_template['operation_template_id'])
    formula_task_id = int(task_template['formula_task_id'])
    node_index = task_template['node_index']

    session['tree_template_id'] = int(task_template['tree_template_id'])
    tree_template_all_data = get_tree_template_data(
        connection, session['tree_template_id']).to_dict('records')[0]

    url_template_tree = url_for(
        'tree_template_edit', tree_template_id=session['tree_template_id'], is_directly=0)
    tree_template_all_data = get_tree_template_data(
        connection, session['tree_template_id']).to_dict('records')[0]
    tree_template_data = f'''
        {tree_template_all_data['tree_type_name']}, {tree_template_all_data['key_template_name']} ключ, 
        высота {tree_template_all_data['tree_template_height']}, ключей {tree_template_all_data['tree_template_keys_amount']}, 
        сложность {tree_template_all_data['tree_template_difficulty']}
    '''
    tree_type_id = tree_template_all_data['tree_type_id']
    key_template_id = tree_template_all_data['key_template_id']
    tree_template_height = tree_template_all_data['tree_template_height']
    tree_template_keys_amount = tree_template_all_data['tree_template_keys_amount']
    tree_structure = tree_template_all_data['tree_structure']

    if request.method == 'GET':
        if request.values.get('tree_template_id'):
            session['tree_template_id'] = int(
                request.values.get('tree_template_id'))
            url_template_tree = url_for(
                'tree_template_edit', tree_template_id=session['tree_template_id'], is_directly=0)
            tree_template_all_data = get_tree_template_data(
                connection, session['tree_template_id']).to_dict('records')[0]
            tree_template_data = f'''
                {tree_template_all_data['tree_type_name']}, {tree_template_all_data['key_template_name']} ключ, 
                высота {tree_template_all_data['tree_template_height']}, ключей {tree_template_all_data['tree_template_keys_amount']}, 
                сложность {tree_template_all_data['tree_template_difficulty']}
            '''
            tree_type_id = tree_template_all_data['tree_type_id']
            key_template_id = tree_template_all_data['key_template_id']
            tree_template_height = tree_template_all_data['tree_template_height']
            tree_template_keys_amount = tree_template_all_data['tree_template_keys_amount']
    elif request.method == 'POST':
        if request.values.get('tree_template_id'):
            session['tree_template_id'] = int(
                request.values.get('tree_template_id'))
            url_template_tree = url_for(
                'tree_template_edit', tree_template_id=session['tree_template_id'], is_directly=0)
            tree_template_all_data = get_tree_template_data(
                connection, session['tree_template_id']).to_dict('records')[0]
            tree_template_data = f'''
                {tree_template_all_data['tree_type_name']}, {tree_template_all_data['key_template_name']} ключ, 
                высота {tree_template_all_data['tree_template_height']}, ключей {tree_template_all_data['tree_template_keys_amount']}, 
                сложность {tree_template_all_data['tree_template_difficulty']}
            '''
            tree_type_id = tree_template_all_data['tree_type_id']
            key_template_id = tree_template_all_data['key_template_id']
            tree_template_height = tree_template_all_data['tree_template_height']
            tree_template_keys_amount = tree_template_all_data['tree_template_keys_amount']
        if 'save_template' in request.form:
            session['tree_template_id'] = int(
                request.values.get('tree_template_id'))
            task_template_difficulty = request.form.get(
                'task_template_difficulty')
            operation_template_id = int(
                request.form.get('operation_template_id'))
            formula_task_id = int(request.form.get('formula_task_id'))

            data_tuple = (task_template_difficulty, )
            func_tuple = (float,)

            handled_data = [
                transform_num_data(func, data)
                for func, data in zip(func_tuple, data_tuple)
            ]

            if all(handled_data):
                update_difficulty(connection, task_template_id,
                                  task_template_difficulty)
                flash("Шаблон обновлен!")
            else:
                flash("Введите все необходимые данные!")

        if 'del_template' in request.form:
            del_task_template(connection, task_template_id)
            flash("Шаблон удален!")
            return redirect(url_for('task_template', is_directly=is_directly))

    test_url = session.get('test_url')

    df_operations = get_operations(connection, tree_type_id)
    operation_indexes = tuple(df_operations['operation_template_id'])
    operation_values = tuple(df_operations['operation_name'])

    df_formulas = get_formulas(connection)
    formula_indexes = tuple(df_formulas['formula_task_id'])
    formula_pictures = tuple(
        formula_task[formula_id]['picture'] for formula_id in formula_task)

    html = render_template(
        'teacher_module/task_template_edit.html',
        operation_indexes=operation_indexes,
        operation_values=operation_values,
        zip=zip,
        operation_template_id=operation_template_id,
        url_template_tree=url_template_tree,
        tree_template_data=tree_template_data,
        tree_template_id=session['tree_template_id'],
        formula_indexes=formula_indexes,
        formula_pictures=formula_pictures,
        formula_task_id=formula_task_id,
        tree_type_id=tree_type_id,
        key_template_id=key_template_id,
        tree_template_height=tree_template_height,
        tree_template_keys_amount=tree_template_keys_amount,
        task_template_difficulty=task_template_difficulty,
        disable_data=disable_data,
        is_directly=is_directly,
        test_url=test_url,
        tree_structure=tree_structure,
        node_index=node_index,
        user_name=session['user_name'],
    )

    return html
