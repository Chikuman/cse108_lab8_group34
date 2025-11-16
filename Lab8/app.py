# app.py
from flask import Flask, render_template
from data_structures import db, login_manager  # extensions
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


    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        # show login page, or redirect if you want
        return render_template("login.html")

    @app.route("/index")
    def index():
        return render_template("index.html")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
