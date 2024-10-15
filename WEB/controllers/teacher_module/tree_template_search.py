from app import app, DATABASE_NAME, SEPARATOR
from flask import render_template, request, session
from utils import get_db_connection
from models.teacher_module.tree_template_search_model import *


@app.route('/Шаблон-дерева/Поиск/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Шаблон-дерева/Поиск/<int:is_directly>', methods=['GET', 'POST'])
def tree_template_search(is_directly):
    connection = get_db_connection(DATABASE_NAME)

    ################################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    ################################
    task_url = session.get('task_url')
    teacher_id = session['teacher_id']

    _tree_height = (3, 4, 5)
    _node_count_min = 3
    _node_count_max = 31
    _key_templates = get_key_templates(connection)
    _tree_types = get_tree_types(connection)
    _difficulty_max = 1.0
    _difficulty_min = 0.0

    tree_height = ()
    node_count_from = None
    node_count_to = None
    key_template_ids = ()
    tree_type_ids = ()
    difficulty_from = None
    difficulty_to = None

    if request.method == 'POST':
        if 'filter' in request.form:
            tree_height = request.form.getlist('tree_height')
            node_count_from = request.form.get('node_count_from')
            node_count_to = request.form.get('node_count_to')
            key_template_ids = request.form.getlist('key_template_ids')
            difficulty_from = request.form.get('difficulty_from')
            difficulty_to = request.form.get('difficulty_to')
            tree_type_ids = request.form.getlist('tree_type_ids')

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
        if 'clear' in request.form:
            tree_height = ()
            node_count_from = None
            node_count_to = None
            key_template_ids = ()
            tree_type_ids = ()
            difficulty_from = None
            difficulty_to = None

    df_my_tree_templates = get_my_tree_templates(
        connection,
        teacher_id,
        tree_height if tree_height else _tree_height,
        node_count_from if node_count_from else _node_count_min,
        node_count_to if node_count_to else _node_count_max,
        key_template_ids if key_template_ids else tuple(
            map(lambda x: x[0], _key_templates)),
        tree_type_ids if tree_type_ids else tuple(
            map(lambda x: x[0], _tree_types)),
        difficulty_from if difficulty_from else _difficulty_min,
        difficulty_to if difficulty_to else _difficulty_max
    )
    my_tree_templates = df_my_tree_templates.to_dict('records')

    df_other_tree_templates = get_other_tree_templates(
        connection,
        teacher_id,
        tree_height if tree_height else _tree_height,
        node_count_from if node_count_from else _node_count_min,
        node_count_to if node_count_to else _node_count_max,
        key_template_ids if key_template_ids else tuple(
            map(lambda x: x[0], _key_templates)),
        tree_type_ids if tree_type_ids else tuple(
            map(lambda x: x[0], _tree_types)),
        difficulty_from if difficulty_from else _difficulty_min,
        difficulty_to if difficulty_to else _difficulty_max
    )
    other_tree_templates = df_other_tree_templates.to_dict('records')

    html = render_template(
        'teacher_module/tree_template_search.html',
        my_tree_templates=my_tree_templates,
        other_tree_templates=other_tree_templates,
        is_directly=is_directly,
        task_url=task_url,
        _tree_height=_tree_height,
        _key_templates=_key_templates,
        _tree_types=_tree_types,
        _difficulty_max=_difficulty_max,
        _difficulty_min=_difficulty_min,
        _node_count_min=_node_count_min,
        _node_count_max=_node_count_max,
        tree_height=tree_height,
        key_template_ids=key_template_ids,
        tree_type_ids=tree_type_ids,
        node_count_from=node_count_from,
        node_count_to=node_count_to,
        difficulty_from=difficulty_from,
        difficulty_to=difficulty_to,
        SEPARATOR=SEPARATOR,
        user_name=session['user_name'],
    )

    return html
