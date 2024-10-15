from flask import render_template
from app import app

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', text='Страница не найдена'), 404

@app.errorhandler(500)
def not_found(error):
    return render_template('error.html', text='Прозошла ошибка'), 500