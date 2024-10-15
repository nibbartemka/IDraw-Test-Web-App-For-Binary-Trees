from app import app, DATABASE_NAME
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection
from models.teacher_module.subgroup_search_model import *


@app.route('/Подгруппы/Поиск/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Подгруппы/Поиск/<int:is_directly>', methods=['GET', 'POST'])
def subgroup_search(is_directly):
    connection = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    # После реализации авторизации удалить
    teacher_id = session['teacher_id']
    testing_session_url = session.get('testing_session_url')

    groups = get_groups(connection).to_dict('records')

    _group_ids = tuple(item['group_id'] for item in groups)
    checked_groups = ()

    if request.method == 'POST':
        if 'filter' in request.form:
            checked_groups = request.values.getlist('group_id')
            if checked_groups:
                checked_groups = tuple(map(int, checked_groups))

    my_subgroups = get_my_subgroups(
        connection,
        teacher_id,
        (*checked_groups, checked_groups[0]) if checked_groups else _group_ids
    ).to_dict('records')
    other_subgroups = get_other_subgroups(
        connection,
        teacher_id,
        (*checked_groups, checked_groups[0]) if checked_groups else _group_ids
    ).to_dict('records')

    html = render_template(
        'teacher_module/subgroup_search.html',
        my_subgroups=my_subgroups,
        other_subgroups=other_subgroups,
        is_directly=is_directly,
        testing_session_url=testing_session_url,
        checked_values=session.get('subgroup_ids'),
        groups=groups,
        checked_groups=checked_groups,
        user_name=session['user_name'],

    )
    return html
