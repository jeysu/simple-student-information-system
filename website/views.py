from flask import Blueprint, render_template

views = Blueprint('route', __name__)

@views.route('')
def students():
    return render_template("students.html")

@views.route('courses')
def courses():
    return render_template("courses.html")