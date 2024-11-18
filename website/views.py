from flask import Blueprint, render_template, request, flash, jsonify
from .models import Students
from . import db
import re

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

        if not all([id_number, first_name, last_name, year_level, course, sex]):
            flash('All fields are required', 'error')
        elif not re.match(r'^\d{4}-\d{4}$', id_number):
            flash('ID Number must be in format XXXX-XXXX (e.g., 2024-0001)', category='error')
        elif re.search(r'\d', first_name):
            flash('First name should not contain numbers', 'error')
        elif re.search(r'\d', last_name):
            flash('Last name should not contain numbers', 'error')
        else:
            new_student = Students(id_number=id_number, last_name=last_name, first_name=first_name, year_level=year_level, course=course, sex=sex)
            db.session.add(new_student)
            db.session.commit()
            flash('New student added successfully', 'success')
            
    students = Students.query.order_by(Students.id_number).all()
    return render_template("students.html", students=students)

@views.route('/delete-student/<id_number>', methods=['DELETE'])
def delete_student(id_number):
    try:
        student = Students.query.filter_by(id_number=id_number).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Student not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@views.route('courses')
def courses():
    return render_template("courses.html")