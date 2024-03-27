from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from .extensions import db
import bcrypt

auth = Blueprint('auth', __name__)

# Put your authentication routes here
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        flash('You are already logged in.')
        return redirect(url_for('admin.admin_dashboard'))  # Or wherever you want to redirect users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.checkpw(password, user.password.encode('utf-8')):
            session['username'] = user.username
            session['user_type'] = user.user_type
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.')
            return redirect(url_for('auth.login'))
    return render_template('login.html')  # Ensure you have a login.html template


@auth.route('/logout')
def logout():
    # Remove the username from the session if it's there
    session.pop('username', None)
    # Redirect to login page or home page after logout
    return redirect(url_for('index'))  # Assuming you have a view function named 'login'


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
        user_type = request.form['user_type']  # Ensure this comes from your registration form
        
        new_user = User(username=username, password=password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()
        
        flash('User registered successfully!')
        return redirect(url_for('auth.login'))
    return render_template('register.html') 