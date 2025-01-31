from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User
from . import auth_bp
from flask_login import login_user, logout_user, login_required
from datetime import datetime, timedelta
from flask_login import current_user, login_user
from forms import LoginForm, RegisterForm


@auth_bp.route('/terms', methods=['GET', 'POST'])
@login_required  # Ensure only authenticated users can access
def terms():
    """
    Page displaying Terms & Conditions (T&C).
    Users must agree to proceed if they haven't already.
    """
    if request.method == 'POST':
        current_user.terms_accepted = True
        db.session.commit()
        return redirect(url_for('dashboard_bp.dashboard'))   # Ensure 'dashboard' is a registered route

    return render_template('terms.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Simple registration:
    - Must accept T&C for GDPR compliance.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        phone = form.phone_number.data
        terms_accepted = form.accept_terms.data

        existing_user = User.query.filter_by(phone_number=phone).first()
        if existing_user:
            return redirect(url_for('auth.login'))  # Fix redirect to correct login

        # Create new user
        new_user = User(phone_number=phone, terms_accepted=terms_accepted)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        login_user(new_user)  # Auto-login after registration
        return redirect(url_for('dashboard_bp.dashboard'))  # Ensure 'dashboard' is correct

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login route.
    Redirects authenticated users to the dashboard.
    """
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('dashboard_bp.dashboard'))

    if form.validate_on_submit():
        phone = form.phone_number.data
        user = User.query.filter_by(phone_number=phone).first()

        if not user:
            return render_template('login.html', form=form, error="User not found. Please register.")

        login_user(user)  # Use Flask-Login to handle authentication
        return redirect(url_for('dashboard_bp.dashboard'))

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """
    Logs out the user and redirects to the home page.
    """
    logout_user()
    session.clear()
    return redirect(url_for('index'))  # Ensure 'index' exists