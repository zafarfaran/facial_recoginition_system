from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .auth import auth
from .admin import admin
from flask import render_template
from .extensions import db

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:8080/facial_recognition_db'
    # Additional configuration settings for your app
    app.secret_key = 'your_secret_key'

    db.init_app(app)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')
    # Import models here to ensure they are known to SQLAlchemy
    from .models import User, Attendance, Student, Course, Subject
    @app.route('/') 
    def index():
        return render_template('index.html')

    return app

