from app import app, DATABASE_NAME
from flask import render_template, request, flash, session, redirect, url_for
from utils import get_db_connection, formula_task
from models.student_module.task_pass_module import *
from datetime import date, datetime, timedelta
import json
from apscheduler.schedulers.background import BackgroundScheduler
import os

# if not os.path.exists(DATABASE_NAME):
#     connection = get_db_connection(DATABASE_NAME)
#     cursor = connection.cursor()
#     db_init(cursor)


# def update_data_every_minute():

#     conn = get_db_connection(DATABASE_NAME)
#     testing_session_student = get_all_testing_session_student(conn)
#     student_tuples = [tuple(row) for row in testing_session_student.to_numpy()]

#     for student_testing in student_tuples:
#         update_bd_every_minute(conn, student_testing[0], student_testing[1])


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=update_data_every_minute, trigger="interval", minutes=1)
# scheduler.start()


@app.route('/Прохождение-сеанса-тестирования/<int:testing_session_id>', methods=['GET', 'POST'])
def task_pass(testing_session_id):

    conn = get_db_connection(DATABASE_NAME)
    is_last = False
    test_mark = -1
    end_text = ''
    if 'task_index' not in session:
        session['task_index'] = 0

    ##############################
    if not session.get('student_id'):
        session['student_id'] = 1
    # После реализации авторизации удалить

    test_tasks = get_test_tasks(conn, testing_session_id).to_dict('records')

    task_template_id = test_tasks[session['task_index']]['task_template_id']

    task_info = get_task_info(conn, testing_session_id,
                              task_template_id).to_dict('records')[0]

    test_id = get_test_id(
        conn, session['student_id'], testing_session_id)['test_id'].tolist()[0]

    if not session['task_index']:
        session['task_marks'] = [0 for _ in range(len(test_tasks))]

    # operation_template_id = task_info['operation_template_id']

    if request.method == 'POST':

        if 'begin_testing' in request.form:
            session['current_time'] = (datetime.now()).strftime("%H:%M")
            update_into_test_begin(
                conn, session['current_time'], session['student_id'], testing_session_id)

        if 'complete' in request.form:

            tasks_index = session['task_index']

            print(request.values)

            if request.values.get('suboperation_error_count'):
                print('АГА')
                error_count_dict = json.loads(
                    request.values.get('suboperation_error_count'))
                n = int(request.values.get('step_count'))
                mi_s = error_count_dict.values()
                formula_body = task_info['formula_task_body']
                task_mark = round(eval(formula_body), 2)
                session['task_marks'][session['task_index']] = task_mark
                session['task_index'] = session.get('task_index') + 1
                add_into_task(conn, task_template_id, test_id,
                              task_info['tree_template_id'], task_mark)
                tasks_index += 1

            for i in session['task_marks'][session['task_index']:]:

                task_template_id = test_tasks[tasks_index]['task_template_id']
                tasks_index += 1
                add_into_task(conn, task_template_id, test_id,
                              task_info['tree_template_id'], i)

            is_last = True
            test_info = get_test_info(conn, testing_session_id)
            formula_body = test_info['formula_test_body'].tolist()[0]
            B = test_info['test_template_bar'].tolist()[0]
            task_difficulties = test_info['task_difficulties'].tolist()[
                0].split(';')
            zi_s = list(map(float, task_difficulties))
            ri_s = session['task_marks']
            test_mark = round(eval(formula_body), 2)
            session['current_date'] = (date.today()).strftime('%Y-%m-%d')
            session['current_time'] = (datetime.now()).strftime("%H:%M")
            add_into_test_end(
                conn, test_mark, session['current_date'], session['current_time'], test_id)

        if 'next_task' in request.form:

            session['current_time'] = (datetime.now()).strftime("%H:%M")
            df_description = get_discription_testing_session(
                conn, testing_session_id).to_dict('records')

            if len(test_tasks) == session['task_index']+1:

                error_count_dict = json.loads(
                    request.values.get('suboperation_error_count'))
                n = int(request.values.get('step_count'))
                mi_s = error_count_dict.values()
                formula_body = task_info['formula_task_body']
                task_mark = round(eval(formula_body), 2)
                session['task_marks'][session['task_index']] = task_mark
                session['task_index'] = session.get('task_index') + 1
                add_into_task(conn, task_template_id, test_id,
                              task_info['tree_template_id'], task_mark)
                is_last = True
                test_info = get_test_info(conn, testing_session_id)
                formula_body = test_info['formula_test_body'].tolist()[0]
                B = test_info['test_template_bar'].tolist()[0]
                task_difficulties = test_info['task_difficulties'].tolist()[
                    0].split(';')
                zi_s = list(map(float, task_difficulties))
                ri_s = session['task_marks']
                test_mark = round(eval(formula_body), 2)
                session['current_date'] = (date.today()).strftime('%Y-%m-%d')
                session['current_time'] = (datetime.now()).strftime("%H:%M")
                add_into_test_end(
                    conn, test_mark, session['current_date'], session['current_time'], test_id)

            elif session['current_time'] > df_description[0]['testing_session_end_time']:
                tasks_index = session['task_index']

                error_count_dict = json.loads(
                    request.values.get('suboperation_error_count'))
                n = int(request.values.get('step_count'))
                mi_s = error_count_dict.values()
                formula_body = task_info['formula_task_body']
                task_mark = round(eval(formula_body), 2)
                session['task_marks'][session['task_index']] = task_mark
                session['task_index'] = session.get('task_index') + 1
                add_into_task(conn, task_template_id, test_id,
                              task_info['tree_template_id'], task_mark)
                tasks_index += 1

                for i in session['task_marks'][session['task_index']:]:

                    task_template_id = test_tasks[tasks_index]['task_template_id']
                    tasks_index += 1
                    add_into_task(conn, task_template_id, test_id,
                                  task_info['tree_template_id'], i)

                is_last = True
                test_info = get_test_info(conn, testing_session_id)
                formula_body = test_info['formula_test_body'].tolist()[0]
                B = test_info['test_template_bar'].tolist()[0]
                task_difficulties = test_info['task_difficulties'].tolist()[
                    0].split(';')
                zi_s = list(map(float, task_difficulties))
                ri_s = session['task_marks']
                test_mark = round(eval(formula_body), 2)
                session['current_date'] = (date.today()).strftime('%Y-%m-%d')
                session['current_time'] = (datetime.now()).strftime("%H:%M")
                add_into_test_end(
                    conn, test_mark, session['current_date'], session['current_time'], test_id)
                end_text = 'Время вышло!'

            else:
                print("ПОПАЛСЯ")
                error_count_dict = json.loads(
                    request.values.get('suboperation_error_count'))
                n = int(request.values.get('step_count'))
                mi_s = error_count_dict.values()
                formula_body = task_info['formula_task_body']
                task_mark = round(eval(formula_body), 2)
                session['task_marks'][session['task_index']] = task_mark
                session['task_index'] = session.get('task_index') + 1
                add_into_task(conn, task_template_id, test_id,
                              task_info['tree_template_id'], task_mark)

    if not is_last:

        task_template_id = test_tasks[session['task_index']
                                      ]['task_template_id']

        task_info = get_task_info(conn, testing_session_id,
                                  task_template_id).to_dict('records')[0]

        test_id = get_test_id(
            conn, session['student_id'], testing_session_id)['test_id'].tolist()[0]

        operation_template_id = task_info['operation_template_id']

        operation_data = get_operation(
            conn, operation_template_id, task_template_id).to_json(orient='records')

        suboperation_data = get_suboperations(
            conn, operation_template_id).to_json(orient='records')

        tree_structure = task_info['tree_structure']
        key_template_id = task_info['key_template_id']
        tree_type_id = task_info['tree_type_id']
        tree_template_height = task_info['tree_template_height']

    else:
        test_id = None
        operation_template_id = None
        operation_data = None
        suboperation_data = None
        tree_structure = None
        key_template_id = None
        tree_type_id = None
        tree_template_height = None
        print(session['task_index'])

        print(task_info)
    html = render_template(
        'student_module/task_pass.html',
        tree_structure=tree_structure,
        key_template_id=key_template_id,
        tree_type_id=tree_type_id,
        tree_template_height=tree_template_height,
        testing_session_id=testing_session_id,
        is_last=is_last,
        task_index=session['task_index']+1,
        enumerate=enumerate,
        operation_data=operation_data,
        suboperation_data=suboperation_data,
        test_mark=test_mark,
        user_name=session['user_name'],
        block=True,
        tasks_count=len(test_tasks),
        end_text=end_text
    )

    return html
