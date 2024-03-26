from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from .extensions import db

import bcrypt
from functools import wraps


admin = Blueprint('admin', __name__)
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'user_type' in session or session['user_type'] != 'admin':
            flash('This page is restricted to admin users.')
            return redirect(url_for('auth.login'))  # Redirect to login or another appropriate page
        return f(*args, **kwargs)
    return decorated_function

# Put your authentication routes here
@admin.route('/adminDashboard', methods=['GET', 'POST'])
@admin_required
def admin_dashboard():
    return render_template('admin-dashboard.html')
    pass

