from app import app, DATABASE_NAME
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection
from models.teacher_module.tree_template_model import *


def transform_data(func, data):
    res = None

    if (func == str):
        return func(data)

    try:
        res = float(data)
        res = func(res)
    except Exception:
        pass

    return res


@app.route('/Шаблон-дерева/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Шаблон-дерева/<int:is_directly>', methods=['GET', 'POST'])
def tree_template(is_directly):
    connection = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    # После реализации авторизации удалить
    teacher_id = session['teacher_id']

    tree_type_id = None
    key_template_id = None
    tree_height = None
    node_count = None
    tree_difficulty = None
    tree_structure = ''

    if request.method == 'POST':
        if 'generate_new' in request.form:
            tree_structure = ''
            tree_type_id = int(request.values.get('tree_type_id'))
            key_template_id = int(request.values.get('key_template_id'))
            tree_height = request.values.get('tree_height')
            node_count = request.values.get('node_count')
            tree_difficulty = request.values.get('tree_difficulty')

        if 'save_template' in request.form:
            tree_type_id = int(request.values.get('tree_type_id'))
            key_template_id = int(request.values.get('key_template_id'))
            tree_height = request.values.get('tree_height')
            node_count = request.values.get('node_count')
            tree_difficulty = request.values.get('tree_difficulty')
            tree_structure = request.values.get('tree_structure')

            data_tuple = (tree_type_id, key_template_id, tree_height,
                          node_count, tree_structure, tree_difficulty)
            func_tuple = (int, int, int, int, str, float)

            handled_data = [
                transform_data(func, data)
                for func, data in zip(func_tuple, data_tuple)
            ]

            if all(handled_data):
                handled_data.append(teacher_id)
                tree_template_id = add_tree_template(connection, handled_data)

                if tree_template_id:
                    flash(
                        f"Шаблон успешно создан! <a href={url_for('tree_template_edit', tree_template_id=tree_template_id, is_directly=is_directly)}>Перейти к шаблону</a>")
                    return redirect(url_for('tree_template', is_directly=is_directly))
                else:
                    flash("Шаблон с такими параметрами уже есть в системе!")
            else:
                flash("Введите все необходимые данные!")

    df_tree_type = get_tree_type(connection)

    type_indexes = tuple(df_tree_type['tree_type_id'])
    type_values = tuple(df_tree_type['tree_type_name'])

    df_key_template = get_key_template(connection)

    key_indexes = tuple(df_key_template['key_template_id'])
    key_values = tuple(df_key_template['key_template_name'])

    html = render_template(
        'teacher_module/tree_template.html',
        type_indexes=type_indexes,
        type_values=type_values,
        key_indexes=key_indexes,
        key_values=key_values,
        zip=zip,
        tree_type_id=tree_type_id,
        key_template_id=key_template_id,
        tree_height=tree_height,
        node_count=node_count,
        tree_difficulty=tree_difficulty,
        task_url=session.get('task_url'),
        is_directly=is_directly,
        tree_structure=tree_structure,
        user_name=session['user_name'],
    )

    return html


@app.route('/Шаблон-дерева/<int:tree_template_id>/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Шаблон-дерева/<int:tree_template_id>/<int:is_directly>', methods=['GET', 'POST'])
def tree_template_edit(tree_template_id, is_directly):
    connection = get_db_connection(DATABASE_NAME)

    tree_template = get_tree_template(connection, tree_template_id).loc[0]

    disable_data = check_tree_template_include(connection, tree_template_id)

    #########################################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    #########################################

    teacher_id = session['teacher_id']
    disable_data = [
        'tree_type_id',
        'key_template_id',
        'tree_height',
        'node_count',
        'tree_difficulty'
    ] if (tree_template['teacher_id'] != teacher_id) else disable_data
    # print(disable_data, tree_template['teacher_id'], teacher_id)

    tree_type_id = tree_template['tree_type_id']
    key_template_id = tree_template['key_template_id']
    tree_height = tree_template['tree_template_height']
    node_count = tree_template['tree_template_keys_amount']
    tree_difficulty = tree_template['tree_template_difficulty']
    tree_structure = tree_template['tree_structure']

    if request.method == 'POST':
        tree_type_id = int(request.values.get('tree_type_id'))
        key_template_id = int(request.values.get('key_template_id'))
        tree_height = request.values.get('tree_height')
        node_count = request.values.get('node_count')
        tree_difficulty = request.values.get('tree_difficulty')
        tree_structure = request.values.get('tree_structure')

        data_tuple = (tree_type_id, key_template_id, tree_height,
                      node_count, tree_structure, tree_difficulty)
        func_tuple = (int, int, int, int, str, float)

        handled_data = [
            transform_data(func, data)
            for func, data in zip(func_tuple, data_tuple)
        ]

        if 'generate_new' in request.form:
            tree_structure = ''

        if 'save_template' in request.form:
            if all(handled_data):
                update_tree_template(
                    connection, tree_template_id, handled_data)
                flash("Шаблон обновлен!")
            else:
                # if not disable_data:
                flash("Введите все необходимые данные!")
                # else:
                #     difficulty = handled_data[-1]
                #     update_difficulty(connection, tree_template_id, difficulty)

        elif 'del_template' in request.form:
            del_tree_template(connection, tree_template_id)
            flash("Шаблон удален!")

            return redirect(url_for('tree_template', is_directly=is_directly))

    df_tree_type = get_tree_type(connection)
    type_indexes = tuple(df_tree_type['tree_type_id'])
    type_values = tuple(df_tree_type['tree_type_name'])

    df_key_template = get_key_template(connection)
    key_indexes = tuple(df_key_template['key_template_id'])
    key_values = tuple(df_key_template['key_template_name'])

    html = render_template(
        'teacher_module/tree_template_edit.html',
        type_indexes=type_indexes,
        type_values=type_values,
        key_indexes=key_indexes,
        key_values=key_values,
        zip=zip,
        tree_type_id=tree_type_id,
        key_template_id=key_template_id,
        tree_height=tree_height,
        node_count=node_count,
        tree_difficulty=tree_difficulty,
        disable_data=disable_data,
        is_directly=is_directly,
        task_url=session.get('task_url'),
        tree_structure=tree_structure,
        user_name=session['user_name'],
    )

    return html
