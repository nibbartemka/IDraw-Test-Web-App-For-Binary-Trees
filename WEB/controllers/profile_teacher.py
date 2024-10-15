from app import app, DATABASE_NAME
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection
from models.authorization_page_module import *
from datetime import date, datetime, timedelta


@app.route('/profile_teacher', methods=['GET', 'POST'])
def profile_teacher():
    conn = get_db_connection(DATABASE_NAME)

    login = get_login_password_teacher(
        conn, session['teacher_id'])['teacher_login'][0]
    password = get_login_password_teacher(
        conn, session['teacher_id'])['teacher_password'][0]

    if request.method == 'POST':

        if 'save' in request.form and request.values.get('full_name') != '':
            set_teacher_name(
                conn, session['teacher_id'], request.values.get('full_name'))
            session['user_name'] = request.values.get('full_name')

    html = render_template(
        'profile_teacher.html',
        user_name=session['user_name'],
        teacher_id=session['teacher_id'],
        login=login,
        password=password
    )

    return html
