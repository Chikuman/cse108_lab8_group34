# app.py
from flask import Flask, render_template, request, jsonify
from flask_login import current_user, login_required
from data_structures import db, login_manager, User, Student, Teacher, Class, Enrollment  # extensions
from mock_data import mockData # mock data
from routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="dev-change-me",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",  # single source of truth
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    login_manager.init_app(app)
    # login_manager.login_view = "auth.login"


    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        # show login page, or redirect if you want
        return render_template("login.html")

    @app.route("/index")
    def index():
        student = Student.query.filter_by(user_id=current_user.id).first()
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()

        role = "student" if student else "teacher"

        studentClasses = (
            db.session.query(Class)
            .join(Enrollment, Enrollment.class_id == Class.class_id)
            .filter(Enrollment.student_id == student.student_id)
            .all()
        ) if student else []

        teacherClasses = Class.query.filter_by(teacher_id=teacher.teacher_id).all() if teacher else []

        allClasses = (
            db.session.query(Class)
            .all()
        )
        print("Current user:", current_user.id)
        print("Student row:", student)

        return render_template(
            "index.html",
            role=role,
            studentClasses=studentClasses,
            teacherClasses=teacherClasses,
            allClasses=allClasses
        )
    
    @app.route("/toggle_class", methods=["POST"])
    def toggle_class():
        data = request.get_json()
        class_id = data["class_id"]

        student = Student.query.filter_by(user_id=current_user.id).first()

        enrollment = Enrollment.query.filter_by(
            student_id=student.student_id,
            class_id=class_id
        ).first()

        if enrollment:
            db.session.delete(enrollment)
            db.session.commit()
            return jsonify({"status": "dropped"})

        else:
            new_enrollment = Enrollment(student_id=student.student_id, class_id=class_id)
            db.session.add(new_enrollment)
            db.session.commit()
            return jsonify({"status": "added"})

    with app.app_context():
        db.create_all()
        # add mock data to database (delete app.db if mockData is updated to refresh database)
        mockData()

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
