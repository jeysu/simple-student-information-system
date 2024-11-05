from flask import Blueprint, render_template

views = Blueprint('route', __name__)

@views.route('/')
def home():
    return render_template("base.html")