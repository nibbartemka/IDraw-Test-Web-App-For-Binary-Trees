from app import app, DATABASE_NAME
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection
from models.authorization_page_module import *
from datetime import date, datetime, timedelta


@app.route('/', methods=['GET', 'POST'])
def authorization():
    conn = get_db_connection(DATABASE_NAME)

    if request.method == 'POST':
        if 'sign' in request.form:

            user_login = request.form['login']
            user_password = request.form['password']
            id_student = get_student_id(conn, user_login, user_password)[
                'student_id'].values
            id_teacher = get_teacher_id(conn, user_login, user_password)[
                'teacher_id'].values

            if len(id_student) != 0:
                session['student_id'] = int(id_student[0])
                session['user_name'] = get_student_id(conn, user_login, user_password)[
                    'student_name'].values[0]
                print(session['user_name'])

                return redirect(url_for('student_index'))

            elif len(id_teacher) != 0:
                session['teacher_id'] = int(id_teacher[0])
                session['user_name'] = get_teacher_id(conn, user_login, user_password)[
                    'teacher_name'].values[0]
                print(session['user_name'])
                return redirect(url_for('testing_session_search'))

            flash('Неверный логин или пароль')

        if 'exit' in request.form:
            session.clear()

    html = render_template(
        'authorization_page.html',
    )

    return html
