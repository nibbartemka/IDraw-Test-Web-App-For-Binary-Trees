from app import app, DATABASE_NAME
from flask import render_template, session
from utils import get_db_connection


@app.route('/Управление-процессом-тестирования', methods=['GET', 'POST'])
def teacher_index():
    connection = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
        session['user_name'] = "Этигел Этигелович"
    # После реализации авторизации удалить
    print(session['user_name'])
    html = render_template(
        'teacher_module/teacher_index.html',
        user_name=session['user_name']
    )

    return html
