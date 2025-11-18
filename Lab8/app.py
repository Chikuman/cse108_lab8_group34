# app.py
from flask import Flask, render_template
from flask_login import current_user
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

        classes = (
            db.session.query(Class)
            .join(Enrollment, Enrollment.class_id == Class.class_id)
            .filter(Enrollment.student_id == student.student_id)
            .all()
        )
        allClasses = (
            db.session.query(Class)
            .all()
        )

        return render_template("index.html", classes=classes, allClasses=allClasses)

    with app.app_context():
        db.create_all()
        # add mock data to database (delete app.db if mockData is updated to refresh database)
        mockData()

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
