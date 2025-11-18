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

    @app.route("/class/<int:class_id>/students")
    @login_required
    def class_students(class_id):
        enrollments = Enrollment.query.filter_by(class_id=class_id).all()

        results = []
        for e in enrollments:
            student = Student.query.get(e.student_id)
            user = User.query.get(student.user_id)

            results.append({
                "name": user.username,
                "grade": e.grade,
                "enrollment_id": e.enrollment_id
            })

        return jsonify(results)
    
    @app.route("/update-grade", methods=["POST"])
    @login_required
    def update_grade():
        data = request.get_json()
        enrollment_id = data["enrollment_id"]
        new_grade = data["grade"]

        enrollment = Enrollment.query.get(enrollment_id)
        if not enrollment:
            return jsonify({"status": "error", "message": "Enrollment not found"}), 404

        enrollment.grade = new_grade
        db.session.commit()

        return jsonify({
            "status": "success",
            "class_id": enrollment.class_id
        })

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
