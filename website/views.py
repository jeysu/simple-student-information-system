from flask import Blueprint, render_template, request, flash

views = Blueprint('route', __name__)

@views.route('', methods=['GET', 'POST'])
def students():
    if request.method == 'POST':
        id_number = request.form.get('id_number')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        year_level = request.form.get('year_level')
        course = request.form.get('course')
        sex = request.form.get('sex')

    return render_template("students.html")

@views.route('courses')
def courses():
    return render_template("courses.html")