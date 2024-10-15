from app import app, DATABASE_NAME, SEPARATOR
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection, formula_task
from models.teacher_module.test_template_search_model import *


@app.route('/Шаблон-теста/Поиск/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Шаблон-теста/Поиск/<int:is_directly>', methods=['GET', 'POST'])
def test_template_search(is_directly):
    connection = get_db_connection(DATABASE_NAME)

    ################################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    ################################

    testing_session_url = session.get('testing_session_url')
    teacher_id = session['teacher_id']

    _key_templates = get_key_templates(connection)
    _tree_types = get_tree_types(connection)
    _operation_template = get_operation_template(connection)

    _difficulty_max = 1.0
    _difficulty_min = 0.0

    _task_count_min = 1
    _task_count_max = 100

    key_template_ids = ()
    tree_type_ids = ()
    operation_template = ()

    difficulty_from = None
    difficulty_to = None

    task_count_from = None
    task_count_to = None

    if request.method == 'POST':
        if 'clear' in request.form:
            key_template_ids = ()
            tree_type_ids = ()
            operation_template = ()
            difficulty_from = None
            difficulty_to = None
            task_count_from = None
            task_count_to = None
            
        if 'filter' in request.form:
            key_template_ids = request.form.getlist('key_template_ids')
            difficulty_from = request.form.get('difficulty_from')
            difficulty_to = request.form.get('difficulty_to')
            tree_type_ids = request.form.getlist('tree_type_ids')
            operation_template = request.form.getlist('operation_template_names')
            task_count_from = request.form.get('task_count_from')
            task_count_to = request.form.get('task_count_to')

            if key_template_ids:
                key_template_ids = tuple(map(int, key_template_ids))
                key_template_ids = (*key_template_ids, key_template_ids[0])
            if tree_type_ids:
                tree_type_ids = tuple(map(int, tree_type_ids))
                tree_type_ids = (*tree_type_ids, tree_type_ids[0])
            if difficulty_from:
                difficulty_from = float(difficulty_from)
            if difficulty_to:
                difficulty_to = float(difficulty_to)
            if task_count_from:
                task_count_from = int(task_count_from)
            if task_count_to:
                task_count_to = int(task_count_to)
            if operation_template:
                operation_template = (*operation_template, operation_template[0])


    df_my_test_templates = get_my_test_templates(
        connection,
        teacher_id,
        key_template_ids if key_template_ids else tuple(map(lambda x: x[0], _key_templates)),
        tree_type_ids if tree_type_ids else tuple(map(lambda x: x[0], _tree_types)),
        operation_template if operation_template else _operation_template,
        difficulty_from if difficulty_from else _difficulty_min,
        difficulty_to if difficulty_to else _difficulty_max,
        task_count_from if task_count_from else _task_count_min,
        task_count_to if task_count_to else _task_count_max
    )
    my_test_templates = df_my_test_templates.to_dict('records')
    for item in my_test_templates:
        item['tasks'] = get_test_tasks(connection, item['test_template_id']).to_dict('records')
    # print(my_test_templates)

    df_other_test_templates = get_other_test_templates(
        connection,
        teacher_id,
        key_template_ids if key_template_ids else tuple(map(lambda x: x[0], _key_templates)),
        tree_type_ids if tree_type_ids else tuple(map(lambda x: x[0], _tree_types)),
        operation_template if operation_template else _operation_template,
        difficulty_from if difficulty_from else _difficulty_min,
        difficulty_to if difficulty_to else _difficulty_max,
        task_count_from if task_count_from else _task_count_min,
        task_count_to if task_count_to else _task_count_max
    )
    other_test_templates = df_other_test_templates.to_dict('records')
    for item in other_test_templates:
        item['tasks'] = get_test_tasks(connection, item['test_template_id']).to_dict('records')


    html = render_template(
        'teacher_module/test_template_search.html',
        _key_templates=_key_templates,
        _tree_types=_tree_types,
        _operation_template=_operation_template,
        _difficulty_max=_difficulty_max,
        _difficulty_min=_difficulty_min,
        _task_count_min=_task_count_min,
        _task_count_max=_task_count_max,
        is_directly=is_directly,
        key_template_ids=key_template_ids,
        tree_type_ids=tree_type_ids,
        operation_template=operation_template,
        difficulty_from=difficulty_from,
        difficulty_to=difficulty_to,
        testing_session_url=testing_session_url,
        my_test_templates=my_test_templates,
        other_test_templates=other_test_templates,
        task_count_from=task_count_from,
        task_count_to=task_count_to,
        SEPARATOR=SEPARATOR,
        user_name=session['user_name'],
    )

    return html