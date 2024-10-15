from app import app, DATABASE_NAME, SEPARATOR
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection, formula_test
from datetime import date, datetime, timedelta
from models.teacher_module.testing_session_model import *


@app.route('/Сеанс-тестирования/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Сеанс-тестирования/<int:is_directly>', methods=['GET', 'POST'])
def testing_session(is_directly):
    connection = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    # После реализации авторизации удалить
    session['testing_session_url'] = request.url
    teacher_id = session['teacher_id']

    test_template = ()

    if request.values.get('test_template_id'):
        session['test_template_id'] = request.values.get('test_template_id')
    elif request.values.get('subgroup_id') and not request.values.get('subgroup_ids'):
        session['subgroup_ids'] = tuple(
            map(int, request.values.getlist('subgroup_id')))
    elif request.values.get('subgroup_ids'):
        session['subgroup_ids'] = tuple(
            map(int, request.values.get('subgroup_ids').split(SEPARATOR)))
    elif not request.values.get('test_template_id') and not request.values.get('subgroup_id'):
        session['test_template_id'] = 0
        session['testing_session_name'] = ''
        session['testing_session_date'] = (date.today()).strftime('%Y-%m-%d')
        session['testing_session_begin_time'] = (
            datetime.now() ).strftime("%H:%M")
        session['testing_session_end_time'] = (
            datetime.now() + timedelta(minutes=45)).strftime("%H:%M")
        session['testing_session_bar'] = ''
        session['subgroup_ids'] = ()
        session['formula_test_id'] = 1

    if request.method == 'POST':
        if 'del_subgroup_id' in request.form:
            deleting_subgroup = int(request.form.get('del_subgroup_id'))
            session['subgroup_ids'] = tuple(int(
                subgroup_id) for subgroup_id in session['subgroup_ids'] if int(subgroup_id) != deleting_subgroup)

        if 'save' in request.form:
            session['test_template_id'] = request.form.get('test_template_id')
            session['testing_session_name'] = request.form.get(
                'testing_session_name')
            session['testing_session_date'] = request.form.get(
                'testing_session_date')
            session['testing_session_begin_time'] = request.form.get(
                'testing_session_begin_time')
            session['testing_session_end_time'] = request.form.get(
                'testing_session_end_time')
            session['testing_session_bar'] = request.form.get(
                'testing_session_bar')
            session['subgroup_ids'] = request.form.get('subgroup_ids')
            session['formula_test_id'] = request.form.get('formula_test_id')

            if all(
                [
                    session[key]
                    for key in ['test_template_id', 'testing_session_name', 'testing_session_date',
                                'testing_session_begin_time', 'testing_session_end_time', 'testing_session_bar', 'subgroup_ids']
                ]
            ):
                session['subgroup_ids'] = tuple(
                    map(int, session['subgroup_ids'].split(SEPARATOR)))
                session['testing_session_bar'] = int(
                    session['testing_session_bar'])
                session['test_template_id'] = int(session['test_template_id'])
                session['formula_test_id'] = int(session['formula_test_id'])

                testing_session_id = add_testing_session(
                    connection,
                    session['test_template_id'],
                    session['testing_session_name'],
                    session['testing_session_date'],
                    session['testing_session_begin_time'],
                    session['testing_session_end_time'],
                    session['testing_session_bar'],
                    session['formula_test_id'],
                    teacher_id
                )

                add_student_testing_session(
                    connection,
                    testing_session_id,
                    (*session['subgroup_ids'], session['subgroup_ids'][0])
                )
                flash(
                    f"Сеанс тестирования успешно создан! <a href={url_for('testing_session_edit', testing_session_id=testing_session_id, is_directly=is_directly)}>Перейти к сеансу</a>")
                return redirect(url_for('testing_session', is_directly=is_directly))
            else:
                flash('Введите все необходимые данные!')

    test_template = get_test_template_data(
        connection, session['test_template_id'])
    subgroups = get_subgroup_data(connection, session['subgroup_ids'])

    df_formulas = get_formulas(connection)
    formula_indexes = tuple(df_formulas['formula_test_id'])
    formula_pictures = tuple(
        formula_test[formula_id]['picture'] for formula_id in formula_test)

    html = render_template(
        'teacher_module/testing_session.html',
        testing_session_name=session['testing_session_name'],
        testing_session_date=session['testing_session_date'],
        testing_session_begin_time=session['testing_session_begin_time'],
        testing_session_end_time=session['testing_session_end_time'],
        test_template_id=session['test_template_id'],
        testing_session_bar=session['testing_session_bar'],
        test_template=test_template,
        subgroup_ids=SEPARATOR.join(
            tuple(map(str, session['subgroup_ids']))) if session.get('subgroup_ids') else '',
        subgroups=subgroups,
        formula_test_id=session['formula_test_id'],
        formula_indexes=formula_indexes,
        formula_pictures=formula_pictures,
        zip=zip,
        SEPARATOR=SEPARATOR,
        user_name=session['user_name'],
    )

    return html


@app.route('/Сеанс-тестирования/<int:testing_session_id>/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Сеанс-тестирования/<int:testing_session_id>/<int:is_directly>', methods=['GET', 'POST'])
def testing_session_edit(testing_session_id, is_directly):
    connection = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    # После реализации авторизации удалить
    session['testing_session_url'] = request.url
    teacher_id = session['teacher_id']

    testing_session = get_testing_session(connection, testing_session_id)

    is_disable = False
    if (testing_session['teacher_id'] != teacher_id) or (is_testing_session_passed(connection, testing_session_id)):
        is_disable = True

    test_template = ()

    if request.values.get('test_template_id'):
        session['test_template_id'] = request.values.get('test_template_id')
    elif request.values.get('subgroup_id') and not request.values.get('subgroup_ids'):
        session['subgroup_ids'] = tuple(
            map(int, request.values.getlist('subgroup_id')))
    elif request.values.get('subgroup_ids'):
        session['subgroup_ids'] = tuple(
            map(int, request.values.get('subgroup_ids').split(SEPARATOR)))
    elif not request.values.get('test_template_id') and not request.values.get('subgroup_id'):
        session['test_template_id'] = testing_session['test_template_id']
        session['testing_session_name'] = testing_session['testing_session_name']
        session['testing_session_date'] = testing_session['testing_session_date']
        session['testing_session_begin_time'] = testing_session['testing_session_begin_time']
        session['testing_session_end_time'] = testing_session['testing_session_end_time']
        session['testing_session_bar'] = testing_session['test_template_bar']
        session['subgroup_ids'] = tuple(
            map(int, testing_session['subgroup_ids'].split(SEPARATOR)))
        session['formula_test_id'] = testing_session['formula_test_id']

    if request.method == 'POST':
        if 'del_subgroup_id' in request.form:
            deleting_subgroup = int(request.form.get('del_subgroup_id'))
            session['subgroup_ids'] = tuple(int(
                subgroup_id) for subgroup_id in session['subgroup_ids'] if int(subgroup_id) != deleting_subgroup)

        if 'save' in request.form:
            session['test_template_id'] = request.form.get('test_template_id')
            session['testing_session_name'] = request.form.get(
                'testing_session_name')
            session['testing_session_date'] = request.form.get(
                'testing_session_date')
            session['testing_session_begin_time'] = request.form.get(
                'testing_session_begin_time')
            session['testing_session_end_time'] = request.form.get(
                'testing_session_end_time')
            session['testing_session_bar'] = request.form.get(
                'testing_session_bar')
            session['subgroup_ids'] = request.form.get('subgroup_ids')
            session['formula_test_id'] = request.form.get('formula_test_id')

            if all(
                [
                    session[key]
                    for key in ['test_template_id', 'testing_session_name', 'testing_session_date',
                                'testing_session_begin_time', 'testing_session_end_time', 'testing_session_bar', 'subgroup_ids']
                ]
            ):
                session['subgroup_ids'] = tuple(
                    map(int, session['subgroup_ids'].split(SEPARATOR)))
                session['testing_session_bar'] = int(
                    session['testing_session_bar'])
                session['test_template_id'] = int(session['test_template_id'])
                session['formula_test_id'] = int(session['formula_test_id'])

                update_testing_session(
                    connection,
                    testing_session_id,
                    session['test_template_id'],
                    session['testing_session_name'],
                    session['testing_session_date'],
                    session['testing_session_begin_time'],
                    session['testing_session_end_time'],
                    session['testing_session_bar'],
                    session['formula_test_id']
                )

                delete_student_testing_session(
                    connection, testing_session_id, (*session['subgroup_ids'], session['subgroup_ids'][0]))
                add_student_testing_session(
                    connection, testing_session_id, (*session['subgroup_ids'], session['subgroup_ids'][0]))

                flash('Сеанс тестирования обновлен!')
            else:
                flash('Введите все необходимые данные!')
        if 'delete' in request.form:
            delete_testing_session(connection, testing_session_id)
            flash('Сеанс тестирования удален!')
            return redirect(url_for('testing_session', is_directly=is_directly))

    test_template = get_test_template_data(
        connection, session['test_template_id'])
    subgroups = get_subgroup_data(connection, session['subgroup_ids'])

    df_formulas = get_formulas(connection)
    formula_indexes = tuple(df_formulas['formula_test_id'])
    formula_pictures = tuple(
        formula_test[formula_id]['picture'] for formula_id in formula_test)

    html = render_template(
        'teacher_module/testing_session_edit.html',
        testing_session_name=session['testing_session_name'],
        testing_session_date=session['testing_session_date'],
        testing_session_begin_time=session['testing_session_begin_time'],
        testing_session_end_time=session['testing_session_end_time'],
        test_template_id=session['test_template_id'],
        testing_session_bar=session['testing_session_bar'],
        test_template=test_template,
        subgroup_ids=SEPARATOR.join(
            tuple(map(str, session['subgroup_ids']))) if session.get('subgroup_ids') else '',
        subgroups=subgroups,
        formula_test_id=session['formula_test_id'],
        formula_indexes=formula_indexes,
        formula_pictures=formula_pictures,
        zip=zip,
        is_disable=is_disable,
        is_directly=is_directly,
        SEPARATOR=SEPARATOR,
        user_name=session['user_name'],
    )

    return html
