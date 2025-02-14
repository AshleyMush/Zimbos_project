from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models import db
from models.user import User
from forms.auth_forms import RegistrationForm, LoginForm
from . import auth_bp
from flask_login import login_user, current_user, logout_user




@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_count = User.query.count()


    # Check if any users exist in the database.
    user_count = User.query.count()
    if user_count == 0:
        role = 'Admin'  # First user becomes Admin
    else:
        role = 'User'

    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('User already exists, please login', 'warning')
            return redirect(url_for('auth_bp.login'))

        new_user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            country=form.country.data,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful', 'success')
        if new_user.role == "Admin":
            return redirect(url_for('dashboard_bp.admin_dashboard'))
        else:
            return redirect(url_for('dashboard_bp.user_dashboard'))

    return render_template('/auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print("Login route accessed")  # Debugging line

    print(f"Checking authentication: {current_user.is_authenticated}")  # Debugging
    if current_user.is_authenticated:
        print("User is already authenticated, redirecting...")
        return redirect_user_based_on_role(current_user.role)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)
            print(f"User logged in: {user.role}")  # Debugging
            flash('Logged in successfully', 'success')
            return redirect_user_based_on_role(user.role)
        else:
            flash('User not found, please register', 'danger')
            return redirect(url_for('auth_bp.register'))

    return render_template('/auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth_bp.login'))


def redirect_user_based_on_role(user_role):
    print(f"Redirecting user with role: {user_role}")  # Debugging line

    if user_role == "Admin":
        return redirect(url_for('dashboard_bp.admin_dashboard'))
    elif user_role == "Moderator":
        return redirect(url_for('dashboard_bp.user_dashboard'))
    elif user_role == "User":
        return redirect(url_for('dashboard_bp.user_dashboard'))
    else:
        print("Unknown role, redirecting to login")
        return redirect(url_for('auth_bp.login'))  # Prevent infinite loops if role is unknown
