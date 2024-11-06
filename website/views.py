from flask import Blueprint, render_template

views = Blueprint('route', __name__)

@views.route('/')
def students():
    return render_template("students.html")