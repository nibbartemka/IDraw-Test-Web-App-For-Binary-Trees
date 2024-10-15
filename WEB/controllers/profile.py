from app import app, DATABASE_NAME
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection
from models.profile_module import *
from datetime import date, datetime, timedelta


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    conn = get_db_connection(DATABASE_NAME)
    
    login = get_login_password(
        conn, session['student_id'])['student_login'][0]
    password = get_login_password(
        conn, session['student_id'])['student_password'][0]

    if request.method == 'POST':

        if 'save' in request.form and request.values.get('full_name') != '':
            set_student_name(
                conn, session['student_id'], request.values.get('full_name'))
            session['user_name'] = request.values.get('full_name')

    html = render_template(
        'profile.html',
        login=login,
        password=password,
        user_name=session['user_name'],
        student_id=session['student_id']
    )

    return html
