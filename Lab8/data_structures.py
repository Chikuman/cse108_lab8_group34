#data_structures.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    name = db.Column(db.String, nullable = True)
    password = db.Column(db.String, nullable = False)

    is_admin = db.Column(db.Boolean, default=False, nullable=False)
                         
    def set_password(self, password):
        self.password = password
    def check_password(self, password):
        return self.password == password
    
    def __repr__(self):
        return f'<User {self.name or self.username}>'

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    user = db.relationship('User')
    
    def __repr__(self):
        return f'<Student {self.user.name or self.user.username}>'

class Teacher(db.Model):
    teacher_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    user = db.relationship('User')
    
    def __repr__(self):
        return f'<Teacher {self.user.name or self.user.username}>'

class Class(db.Model):
    class_id = db.Column(db.Integer, primary_key = True)
    class_name = db.Column(db.String(70), nullable = False)
    class_time = db.Column(db.String(50), nullable = False)
    class_capacity = db.Column(db.Integer, nullable = False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.teacher_id'))

    teacher = db.relationship('Teacher', backref='classes')
    enrollments = db.relationship("Enrollment", backref="class")
    
    def __repr__(self):
        return f'<Class {self.class_name}>'

class Enrollment(db.Model):
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'))
    class_id = db.Column(db.Integer, db.ForeignKey('class.class_id'))
    grade = db.Column(db.String(5), nullable=True)

    student = db.relationship("Student", backref="enrollments")
    __table_args__ = (
        db.UniqueConstraint('student_id', 'class_id', name='unique_enrollment'),
    )
    
    def __repr__(self):
        try:
            class_name = db.session.query(Class).filter_by(class_id=self.class_id).first().class_name
        except:
            class_name = "Unknown"
        return f'<Enrollment {self.student.user.name} in {class_name}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
