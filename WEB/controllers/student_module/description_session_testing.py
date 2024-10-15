from app import app, DATABASE_NAME
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection
from models.student_module.description_session_testing_module import *
from datetime import date, datetime, timedelta


@app.route('/Описание-сеанса-тестирования/<int:testing_session_id>', methods=['GET', 'POST'])
def description_session_testing(testing_session_id):
    conn = get_db_connection(DATABASE_NAME)
    time = False
    ##############################
    if not session.get('student_id'):
        session['student_id'] = 1
    # После реализации авторизации удалить

    df_description = get_discription_testing_session(
        conn, testing_session_id).to_dict('records')
    df_tasks_testing_session = get_tasks_testing_session(
        conn, testing_session_id).to_dict('records')

    session['current_date'] = (date.today()).strftime('%Y-%m-%d')
    session['current_time'] = (datetime.now()).strftime("%H:%M")

    if session['current_date'] == df_description[0]['testing_session_date'] and  \
            session['current_time'] >= df_description[0]['testing_session_begin_time'] and \
            session['current_time'] <= df_description[0]['testing_session_end_time']:
        time = True

    add_into_test_begin(conn, session['student_id'], testing_session_id)

    html = render_template(
        'student_module/description_session_testing.html',
        df_description=df_description,
        df_tasks_testing_session=len(df_tasks_testing_session),
        enumerate=enumerate,
        testing_session_id=testing_session_id,
        user_name=session['user_name'],
        student_id=session['student_id'],
        len=len,
        time=time
    )

    return html
