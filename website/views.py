from flask import Blueprint, render_template, request, flash, jsonify
from .models import Students, Courses
from . import db
import re

views = Blueprint('route', __name__)

@views.route('/', methods=['GET', 'POST'])
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

@views.route('/courses', methods=['GET', 'POST'])
def courses():
    if request.method == 'POST':
        course_code = request.form.get('course_code')
        course_description = request.form.get('course_description')

        if not all([course_code, course_description]):
            flash('All fields are required', 'error')
        elif re.search(r'\d', course_code):
            flash('Course code should not contain numbers', 'error')
        elif re.search(r'\d', course_description):
            flash('Course Description should not contain numbers', 'error')
        else:
            new_course = Courses(course_code=course_code, course_description=course_description)
            db.session.add(new_course)
            db.session.commit()
            flash('New course added successfully', 'success')

    courses = Courses.query.order_by(Courses.course_code).all()
    return render_template("courses.html", courses=courses)

@views.route('courses/delete-course/<course_code>', methods=['DELETE'])
def delete_course(course_code):
    try:
        course = Courses.query.filter_by(course_code=course_code).first()
        if course:
            db.session.delete(course)
            db.session.commit()
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Course not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@views.route('/edit-student/<id_number>', methods=['POST'])
def edit_student(id_number):
    try:
        student = Students.query.filter_by(id_number=id_number).first()
        if not student:
            return jsonify({'success': False, 'error': 'Student not found'}), 404

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        year_level = request.form.get('year_level')
        course = request.form.get('course')
        sex = request.form.get('sex')

        if not all([first_name, last_name, year_level, course, sex]):
            return jsonify({'success': False, 'error': 'All fields are required'})
        elif re.search(r'\d', first_name):
            return jsonify({'success': False, 'error': 'First name should not contain numbers'})
        elif re.search(r'\d', last_name):
            return jsonify({'success': False, 'error': 'Last name should not contain numbers'})

        student.first_name = first_name
        student.last_name = last_name
        student.year_level = year_level
        student.course = course
        student.sex = sex

        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@views.route('/edit-course/<course_code>', methods=['POST'])
def edit_course(course_code):
    try:
        course = Courses.query.filter_by(course_code=course_code).first()
        if not course:
            return jsonify({'success': False, 'error': 'Course not found'}), 404

        course_description = request.form.get('course_description')

        if not course_description:
            return jsonify({'success': False, 'error': 'All fields are required'})
        elif re.search(r'\d', course_code):
            return jsonify({'success': False, 'error': 'Course Code should not contain numbers'})
        elif re.search(r'\d', course_description):
            return jsonify({'success': False, 'error': 'Course Description should not contain numbers'})

        course.course_description = course_description
        db.session.commit()
        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500