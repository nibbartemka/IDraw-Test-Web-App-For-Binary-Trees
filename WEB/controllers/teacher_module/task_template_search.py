from app import app, DATABASE_NAME, SEPARATOR
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection, formula_task
from models.teacher_module.task_template_search_model import *


@app.route('/Шаблон-тестового-задания/Поиск/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Шаблон-тестового-задания/Поиск/<int:is_directly>', methods=['GET', 'POST'])
def task_template_search(is_directly):
    connection = get_db_connection(DATABASE_NAME)
    
    ################################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    ################################

    test_url = session.get('test_url')
    teacher_id = session['teacher_id']

    _tree_height = (3, 4, 5)
    _node_count_min = 3
    _node_count_max = 31
    _key_templates = get_key_templates(connection)
    _tree_types = get_tree_types(connection)

    _operation_template = get_operation_template(connection)
    _formula_task = get_formula_task(connection, formula_task)
    _difficulty_max = 1.0
    _difficulty_min = 0.0

    tree_height = ()
    node_count_from = None
    node_count_to = None
    key_template_ids = ()
    tree_type_ids = ()

    operation_template = ()
    formula_for_task = ()
    difficulty_from = None
    difficulty_to = None

    if request.method == 'POST':
        if 'clear' in request.form:
            tree_height = ()
            node_count_from = None
            node_count_to = None
            key_template_ids = ()
            tree_type_ids = ()
            operation_template = ()
            formula_for_task = ()
            difficulty_from = None
            difficulty_to = None

        if 'filter' in request.form:
            tree_height = request.form.getlist('tree_height')
            node_count_from = request.form.get('node_count_from')
            node_count_to = request.form.get('node_count_to')
            key_template_ids = request.form.getlist('key_template_ids')
            difficulty_from = request.form.get('difficulty_from')
            difficulty_to = request.form.get('difficulty_to')
            tree_type_ids = request.form.getlist('tree_type_ids')
            operation_template = request.form.getlist('operation_template_names')
            formula_for_task = request.form.getlist('formula_task_ids')

            if tree_height:
                tree_height = tuple(map(int, tree_height))
                tree_height = (*tree_height, tree_height[0])
            if key_template_ids:
                key_template_ids = tuple(map(int, key_template_ids))
                key_template_ids = (*key_template_ids, key_template_ids[0])
            if tree_type_ids:
                tree_type_ids = tuple(map(int, tree_type_ids))
                tree_type_ids = (*tree_type_ids, tree_type_ids[0])
            if node_count_from:
                node_count_from = int(node_count_from)
            if node_count_to:
                node_count_to = int(node_count_to)
            if difficulty_from:
                difficulty_from = float(difficulty_from)
            if difficulty_to:
                difficulty_to = float(difficulty_to)
            if operation_template:
                operation_template = (*operation_template, operation_template[0])
            if formula_for_task:
                formula_for_task = tuple(map(int, formula_for_task))
                formula_for_task = (*formula_for_task, formula_for_task[0])

    df_my_task_templates = get_my_task_templates(
        connection,
        teacher_id,
        tree_height if tree_height else _tree_height,
        node_count_from if node_count_from else _node_count_min,
        node_count_to if node_count_to else _node_count_max,
        key_template_ids if key_template_ids else tuple(map(lambda x: x[0], _key_templates)),
        tree_type_ids if tree_type_ids else tuple(map(lambda x: x[0], _tree_types)),
        operation_template if operation_template else _operation_template,
        formula_for_task if formula_for_task else tuple(map(lambda x: x[0], (*_formula_task, _formula_task[0]))),
        difficulty_from if difficulty_from else _difficulty_min,
        difficulty_to if difficulty_to else _difficulty_max,
    )
    my_task_templates = df_my_task_templates.to_dict('records')

    df_other_task_templates = get_other_task_templates(
        connection,
        teacher_id,
        tree_height if tree_height else _tree_height,
        node_count_from if node_count_from else _node_count_min,
        node_count_to if node_count_to else _node_count_max,
        key_template_ids if key_template_ids else tuple(map(lambda x: x[0], _key_templates)),
        tree_type_ids if tree_type_ids else tuple(map(lambda x: x[0], _tree_types)),
        operation_template if operation_template else _operation_template,
        formula_for_task if formula_for_task else tuple(map(lambda x: x[0], (*_formula_task, _formula_task[0]))),
        difficulty_from if difficulty_from else _difficulty_min,
        difficulty_to if difficulty_to else _difficulty_max,
    )
    other_task_templates = df_other_task_templates.to_dict('records')


    html = render_template(
        'teacher_module/task_template_search.html',
        _tree_height=_tree_height,
        _node_count_min=_node_count_min,
        _node_count_max=_node_count_max,
        _key_templates=_key_templates,
        _tree_types=_tree_types,
        _operation_template=_operation_template,
        _formula_task=_formula_task,
        _difficulty_max=_difficulty_max,
        _difficulty_min=_difficulty_min,
        is_directly=is_directly,
        tree_height=tree_height,
        node_count_from=node_count_from,
        node_count_to=node_count_to,
        key_template_ids=key_template_ids,
        tree_type_ids=tree_type_ids,
        operation_template=operation_template,
        formula_for_task=formula_for_task,
        difficulty_from=difficulty_from,
        difficulty_to=difficulty_to,
        my_task_templates=my_task_templates,
        other_task_templates=other_task_templates,
        test_url=test_url,
        task_template_ids=session.get('task_template_ids'),
        SEPARATOR=SEPARATOR,
        user_name=session['user_name'],

    )

    return html