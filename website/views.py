from flask import Blueprint

views = Blueprint('route', __name__)

@views.route('/')
def home():
    return '<h1> Test <h1>'