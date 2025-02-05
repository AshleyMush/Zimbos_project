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


    if user_count == 0:
        role = 'Admin'

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
        flash('Registration successful, please login', 'success')
        return redirect(url_for('auth_bp.login'))
    return render_template('/auth/register.html', form=form)







@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()


    if current_user.is_authenticated:
        if current_user.role == "Admin":
            return redirect(url_for('admin_bp.admin_dashboard'))

        elif current_user.role == "Moderator":
            pass
        else:
            return redirect(url_for('dashboard_bp.dashboard_view'))




    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            login_user(user)

            flash('Logged in successfully', 'success')
            if user.role == "Admin":
                return redirect(url_for('admin_bp.admin_dashboard'))

            elif user.role == "Moderator":
                pass
            else:
                return redirect(url_for('dashboard_bp.dashboard_view'))
        else:
            flash('User not found, please register', 'danger')
            return redirect(url_for('auth_bp.register'))
    return render_template('/auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    logout_user()

    return redirect(url_for('auth_bp.login'))
