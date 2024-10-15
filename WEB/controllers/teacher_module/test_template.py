import json
from app import app, DATABASE_NAME, SEPARATOR
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection
from models.teacher_module.test_template_model import *


def transform_num_data(func, data):
    res = None
    
    try:
        res = float(data)
        res = func(res)
    except Exception:
        pass
    
    return res


@app.route('/Шаблон-теста/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Шаблон-теста/<int:is_directly>', methods=['GET', 'POST'])
def test_template(is_directly):
    connection = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    ############################## После реализации авторизации удалить   
    testing_session_url = session.get('testing_session_url')

    teacher_id = session['teacher_id']
    session['test_url'] = request.url
    
    task_templates = ()
    test_template_difficulty = None

    data = {}

    if request.values.getlist('task_template_id') and not request.values.get('task_template_ids'):
        session['task_template_ids'] = tuple(map(int, request.values.getlist('task_template_id')))
        if session['task_template_ids']:
            task_templates = get_task_template_data(connection, (*session['task_template_ids'], session['task_template_ids'][0])).to_dict('records')
    else:
        if request.values.get('task_template_ids'):
            session['task_template_ids'] = tuple(request.values.get('task_template_ids').split(SEPARATOR))
        else:
            session['task_template_ids'] = ()

    if request.method == 'POST':
        if 'del_task_template' in request.form:
            deleting_task_template = int(request.form.get('del_task_template_id'))
            session['task_template_ids'] = tuple(int(task_template_id) for task_template_id in session['task_template_ids'] if int(task_template_id) != deleting_task_template)
            if session['task_template_ids']:
                task_templates = get_task_template_data(connection, (*session['task_template_ids'], session['task_template_ids'][0])).to_dict('records')
        if 'save_template'in request.form:
            session['task_template_ids'] = [int(item) for item in request.values.get('task_template_ids').split(SEPARATOR) if item]
            # session['task_template_ids'] = tuple(
            #     map(
            #         int,
            #         request.values.get('task_template_ids').split(SEPARATOR)
            #     )
            # )
            
            if session['task_template_ids']:
                task_templates = get_task_template_data(
                    connection, 
                    (*session['task_template_ids'], session['task_template_ids'][0]
                )).to_dict('records')

            data = {
                key: request.values.get(f'count_{key}')
                for key in session['task_template_ids']
            }
 
            test_template_difficulty = request.values.get('test_template_difficulty')

            data_tuple = (*data.values(), test_template_difficulty)
            func_tuple = (*[int for _ in data.keys()], float)

            handled_data = [
                transform_num_data(func, data)
                for func, data in zip(func_tuple, data_tuple)
            ]

            if all(handled_data):
                handled_data.append(teacher_id)
                test_template_id = add_test_template(connection, handled_data[-2], handled_data[-1])
                for item in data.items():
                    task_template_id = int(item[0])
                    iterations = int(item[1])

                    for _ in range(iterations):
                        add_task_to_test_template(connection, test_template_id, task_template_id)
                flash(f"Шаблон успешно создан! <a href={url_for('test_template_edit', test_template_id=test_template_id, is_directly=is_directly)}>Перейти к шаблону</a>")
                return redirect(url_for('test_template', is_directly=is_directly))
            else:
                flash("Введите все необходимые данные!")
            
       
    html = render_template(
        'teacher_module/test_template.html',
        task_templates=task_templates,
        task_templates_ids=SEPARATOR.join(
            tuple(map(
                str,
                session['task_template_ids']
            ))
        ),
        test_template_difficulty=test_template_difficulty,
        json_data=json.dumps(data),
        is_directly=is_directly,
        testing_session_url=testing_session_url,
        user_name=session['user_name'],
    )
    
    return html


@app.route('/Шаблон-теста/<int:test_template_id>/', defaults={'is_directly': 1}, methods=['GET', 'POST'])
@app.route('/Шаблон-теста/<int:test_template_id>/<int:is_directly>', methods=['GET', 'POST'])
def test_template_edit(test_template_id, is_directly):
    connection = get_db_connection(DATABASE_NAME)

    ##############################
    if not session.get('teacher_id'):
        session['teacher_id'] = 1
    ############################## После реализации авторизации удалить   
    testing_session_url = session.get('testing_session_url')

    teacher_id = session['teacher_id']
    session['test_url'] = request.url

    disable_type = 1 if check_test_template_include(connection, test_template_id) else 0

    if teacher_id != get_test_teacher_id(connection, test_template_id):
        disable_type = 2
    
    data = get_test_template_data(connection, test_template_id)

    if request.values.getlist('task_template_id') and not request.values.get('task_template_ids'):
        session['task_template_ids'] = tuple(map(int, request.values.getlist('task_template_id')))
        if session['task_template_ids']:
            task_templates = get_task_template_data(connection, (*session['task_template_ids'], session['task_template_ids'][0])).to_dict('records')
    else:
        if request.values.get('task_template_ids'):
            session['task_template_ids'] = tuple(request.values.get('task_template_ids').split(SEPARATOR))
        else:
            session['task_template_ids'] = tuple(data.keys())

    task_templates = get_task_template_data(connection, (*session['task_template_ids'], session['task_template_ids'][0])).to_dict('records')
    test_template_difficulty = get_test_difficulty(connection, test_template_id)

    if request.method == 'POST':
        if 'del_task_template' in request.form:
            deleting_task_template = int(request.form.get('del_task_template_id'))
            session['task_template_ids'] = tuple(int(task_template_id) for task_template_id in session['task_template_ids'] if int(task_template_id) != deleting_task_template)
            if session['task_template_ids']:
                task_templates = get_task_template_data(connection, (*session['task_template_ids'], session['task_template_ids'][0])).to_dict('records')
        if 'save_template'in request.form:
            session['task_template_ids'] = tuple(
                map(
                    int,
                    request.values.get('task_template_ids').split(SEPARATOR)
                )
            )
            
            if session['task_template_ids']:
                task_templates = get_task_template_data(
                    connection, 
                    (*session['task_template_ids'], session['task_template_ids'][0]
                )).to_dict('records')

            data = {
                key: request.values.get(f'count_{key}')
                for key in session['task_template_ids']
            }
 
            test_template_difficulty = request.values.get('test_template_difficulty')

            data_tuple = (*data.values(), test_template_difficulty)
            func_tuple = (*[int for _ in data.keys()], float)

            handled_data = [
                transform_num_data(func, data)
                for func, data in zip(func_tuple, data_tuple)
            ]

            if all(handled_data):
                update_difficulty(connection, test_template_id, handled_data[-1])
                del_test_task_templates(connection, test_template_id)
                for item in data.items():
                    task_template_id = int(item[0])
                    iterations = int(item[1])

                    for _ in range(iterations):
                        add_task_to_test_template(connection, test_template_id, task_template_id)
                flash('Шаблон успешно обновлен!')
                pass
            else:
                flash("Введите все необходимые данные!")
        
        if 'del_template' in request.form:
            del_test_template(connection, test_template_id)
            flash("Шаблон удален!")
            return redirect(url_for('test_template', is_directly=is_directly))
            
       
    html = render_template(
        'teacher_module/test_template_edit.html',
        task_templates=task_templates,
        task_templates_ids=SEPARATOR.join(
            tuple(map(
                str,
                session['task_template_ids']
            ))
        ),
        test_template_difficulty=test_template_difficulty,
        json_data=json.dumps(data),
        disable_type=disable_type,
        is_directly=is_directly,
        testing_session_url=testing_session_url,
        user_name=session['user_name'],
    )
    
    return html