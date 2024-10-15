from app import app, DATABASE_NAME
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection
from models.student_module.main_page_module import *
from models.authorization_page_module import *
from datetime import date, datetime, timedelta
from numpy import isnan


@app.route('/Главная-страница-студент', methods=['GET', 'POST'])
def student_index():
    conn = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('student_id'):
        session['student_id'] = 1
        session['user_name'] = 'Хабиб'
    # После реализации авторизации удалить

    session['task_index'] = 0

    session['current_date'] = (date.today()).strftime('%Y-%m-%d')
    session['current_time'] = (datetime.now()).strftime("%H:%M")

    df_upcoming = get_upcoming_testing_session(
        conn, session['current_date'], session['current_time'], session['student_id']).to_dict('records')

    df_passed = get_passed_testing_session(
        conn, session['current_date'], session['current_time'], session['student_id'])

    df_passed['test_mark'] = df_passed['test_mark'].fillna(-1)
    df_passed = df_passed.to_dict('records')

    html = render_template(
        'student_module/student_index.html',
        df_upcoming=df_upcoming,
        df_passed=df_passed,
        student_id=session['student_id'],
        user_name=session['user_name'],
        SEPARATOR=SEPARATOR,
        int=int
    )

    return html
