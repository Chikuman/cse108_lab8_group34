# app.py
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user, login_required
from data_structures import db, login_manager, User, Student, Teacher, Class, Enrollment  # extensions
from mock_data import mockData # mock data
from routes import auth_bp
import os
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

BASE_DIR = os.path.abspath(os.path.dirname(__file__))



def create_app():
    app = Flask(__name__)
    app.config.update(
    SECRET_KEY="dev-change-me",
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(BASE_DIR, 'instance/app.db')}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

    db.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(auth_bp)
    # login_manager.login_view = "auth.login"

        # ------------- PROTECT ADMIN WITH LOGIN + is_admin -------------
    class SecureAdminIndexView(AdminIndexView):
        def is_accessible(self):
            return current_user.is_authenticated and getattr(current_user, "is_admin", False)

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for("auth.login"))

    class SecureModelView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated and getattr(current_user, "is_admin", False)

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for("auth.login"))

    # ------------- FLASK-ADMIN SETUP -------------
    admin = Admin(
        app,
        name="Admin",
        index_view=SecureAdminIndexView(url="/admin")
    )

    # Expose your models in the admin UI
    admin.add_view(SecureModelView(User, db.session))
    admin.add_view(SecureModelView(Student, db.session))
    admin.add_view(SecureModelView(Teacher, db.session))
    admin.add_view(SecureModelView(Class, db.session))
    admin.add_view(SecureModelView(Enrollment, db.session))


    @app.route("/")
    def home():
        # show login page, or redirect if you want
        return render_template("login.html")


    @app.route("/index")    
    @login_required
    def index():
        # 🔹 If admin hits /index, just send them to Flask-Admin
        if getattr(current_user, "is_admin", False):
            return redirect(url_for("admin.index"))

        student = Student.query.filter_by(user_id=current_user.id).first()
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()

        if student:
            classes = (
                db.session.query(Class)
                .join(Enrollment, Enrollment.class_id == Class.class_id)
                .filter(Enrollment.student_id == student.student_id)
                .all()
            )
            allClasses = db.session.query(Class).all()

            return render_template(
                "index.html",
                mode="student",
                classes=classes,
                allClasses=allClasses,
            )

        elif teacher:
            teacher_classes = (
                db.session.query(Class)
                .filter(Class.teacher_id == teacher.teacher_id)
                .all()
            )

            return render_template(
                "index.html",
                mode="teacher",
                teacher_classes=teacher_classes,
            )

        # 🔹 Fallback only for weird non-admin, non-student, non-teacher accounts
        flash("Your account is not linked to a student or teacher record.", "error")
        return redirect(url_for("auth.logout"))

    
    @app.route("/toggle_class", methods=["POST"])
    @login_required
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


    @app.route("/update_grade", methods=["POST"])
    @login_required
    def update_grade():
        data = request.get_json() or {}
        enrollment_id = data.get("enrollment_id")
        new_grade = data.get("grade", "").strip()

        # Only teachers can update grades
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        if not teacher:
            return jsonify({"error": "Not authorized"}), 403

        if not enrollment_id:
            return jsonify({"error": "Missing enrollment_id"}), 400

        # Make sure the enrollment belongs to one of this teacher's classes
        enrollment = (
            db.session.query(Enrollment)
            .join(Class, Enrollment.class_id == Class.class_id)
            .filter(
                Enrollment.enrollment_id == enrollment_id,
                Class.teacher_id == teacher.teacher_id,
            )
            .first()
        )

        if not enrollment:
            return jsonify({"error": "Enrollment not found or not in your class."}), 404

        enrollment.grade = new_grade or None
        db.session.commit()

        return jsonify({"status": "ok", "grade": enrollment.grade})

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
