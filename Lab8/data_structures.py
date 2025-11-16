#data_structures.py
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"



class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key = True)
    student_name = db.Column(db.String(50), nullable = False)
    def __repr(self):
        return '<Student %r>' % self.id

class Class(db.Model):
    class_id = db.Column(db.Integer, primary_key = True)
    class_name = db.Column(db.String(70), nullable = False)
    class_instructor = db.Column(db.String(50), nullable = False)
    class_time = db.Column(db.String(50), nullable = False)
    class_capacity = db.Column(db.Integer, nullable = False)

    def __repr(self):
        return '<Class %r>' % self.id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)

    def set_password(self, password):
        self.password = password
    def check_password(self, password):
        return self.password == password

    def __repr(self):
        return '<User %r>' % self.id

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
