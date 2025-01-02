from . import db

class Students(db.Model):
    id_number = db.Column(db.String(45), primary_key=True)
    last_name = db.Column(db.String(45))
    first_name = db.Column(db.String(45))
    year_level = db.Column(db.String(45))
    course = db.Column(db.String(45), db.ForeignKey('courses.course_code', onupdate="CASCADE", ondelete="SET NULL"))
    sex = db.Column(db.String(45))

class Courses(db.Model):
    course_code = db.Column(db.String(45), primary_key=True)
    course_description = db.Column(db.String(45))