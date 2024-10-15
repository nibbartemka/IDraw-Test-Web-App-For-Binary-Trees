
from datetime import date, datetime, timedelta
from flask import Flask
import os
from utils import db_init, get_db_connection
from apscheduler.schedulers.background import BackgroundScheduler
DATABASE_NAME = "idraw.sqlite"
SEPARATOR = ';'


app = Flask(
    __name__,
)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from models.student_module.main_page_module import *
import controllers.profile
import controllers.profile_teacher
import controllers.authorization_page
import controllers.student_module.main_page
import controllers.teacher_module.teacher_index
import controllers.teacher_module.tree_template
import controllers.teacher_module.task_template
import controllers.teacher_module.test_template
import controllers.teacher_module.testing_session
import controllers.teacher_module.tree_template_search
import controllers.teacher_module.task_template_search
import controllers.teacher_module.test_template_search
import controllers.teacher_module.testing_session_search
import controllers.teacher_module.subgroup_search
import controllers.student_module.task_pass
import controllers.student_module.description_session_testing
import controllers.error

if not os.path.exists(DATABASE_NAME):
    connection = get_db_connection(DATABASE_NAME)
    cursor = connection.cursor()
    db_init(cursor)


def update_data_every_minute():

    conn = get_db_connection(DATABASE_NAME)
    testing_session_student = get_all_testing_session_student(conn)
    student_tuples = [tuple(row) for row in testing_session_student.to_numpy()]

    for student_testing in student_tuples:
        update_bd_every_minute(conn, student_testing[0], student_testing[1])


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_data_every_minute, trigger="interval", minutes=1)
scheduler.start()
