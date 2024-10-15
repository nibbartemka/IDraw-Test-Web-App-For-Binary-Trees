from app import app, DATABASE_NAME, SEPARATOR
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection
from datetime import date, datetime, timedelta
from models.teacher_module.testing_session_search_model import *


@app.route('/Сеанс-тестирования/Поиск', methods=['GET', 'POST'])
def testing_session_search():
    connection = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
        session['user_name'] = 'Патрик'

    # После реализации авторизации удалить
    teacher_id = session['teacher_id']

    current_date = (date.today()).strftime('%Y-%m-%d')
    current_time = (datetime.now()).strftime("%H:%M")

    left_border_date = ''
    right_border_date = ''

    if request.method == 'POST':
        if 'filter' in request.form:
            left_border_date = request.form.get('left_border_date')
            right_border_date = request.form.get('right_border_date')

    upcoming_testing_session = get_upcoming_testing_session(
        connection, current_date, current_time, teacher_id).to_dict('records')
    if (left_border_date):
        upcoming_testing_session = list(filter(
            lambda item: item['testing_session_date'] >= left_border_date, upcoming_testing_session))
    if (right_border_date):
        upcoming_testing_session = list(filter(
            lambda item: item['testing_session_date'] <= right_border_date, upcoming_testing_session))

    passed_testing_session = get_passed_testing_session(
        connection, current_date, current_time, teacher_id).to_dict('records')
    if (left_border_date):
        passed_testing_session = list(filter(
            lambda item: item['testing_session_date'] >= left_border_date, passed_testing_session))
    if (right_border_date):
        passed_testing_session = list(filter(
            lambda item: item['testing_session_date'] <= right_border_date, passed_testing_session))

    html = render_template(
        'teacher_module/testing_session_search.html',
        upcoming_testing_session=upcoming_testing_session,
        passed_testing_session=passed_testing_session,
        left_border_date=left_border_date,
        right_border_date=right_border_date,
        SEPARATOR=SEPARATOR,
        user_name=session['user_name'],
    )
    return html


@app.route('/Сеанс-тестирования/Успеваемость/<int:testing_session_id>', methods=['GET', 'POST'])
def testing_session_completition(testing_session_id):
    connection = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    # После реализации авторизации удалить
    subgroup_data = get_testing_session_subgroups(
        connection, testing_session_id).to_dict('records')
    subgroup_ids = tuple(map(lambda item: item['subgroup_id'], subgroup_data))
    checked_subgroups = ()

    if request.method == 'POST':
        if 'filter' in request.form:
            checked_subgroups = request.form.getlist('subgroup_ids')
            if checked_subgroups:
                checked_subgroups = tuple(map(int, checked_subgroups))
        if 'clear' in request.form:
            checked_subgroups = ()

    testing_session_completition_data = get_testing_session_completition_data(
        connection,
        testing_session_id,
        (*subgroup_ids, subgroup_ids[0]) if not checked_subgroups else (
            *checked_subgroups, checked_subgroups[0])
    ).to_dict('records')

    print(session['user_name'])
    html = render_template(
        'teacher_module/testing_session_completition.html',
        testing_session_completition_data=testing_session_completition_data,
        subgroup_data=subgroup_data,
        checked_subgroups=checked_subgroups,
        user_name=session['user_name'],

    )
    return html
