from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, User
from . import auth_bp
from flask_login import login_user, logout_user, login_required


@auth_bp.route('/terms', methods=['GET', 'POST'])
def terms():
    """
    Page displaying Terms & Conditions (T&C).
    Users must agree to proceed if they haven't already.
    """
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user.terms_accepted = True
        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('templates/terms.html')



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Simple registration:
    - In a real system, you'd do phone number validation / OTP verification.
    - Must also accept T&C for GDPR compliance.
    """
    if request.method == 'POST':
        phone = request.form.get('phone_number')
        terms_agreed = request.form.get('terms_agreed') == 'on'

        if not terms_agreed:
            return "You must agree to the Terms and Conditions.", 400

        if not phone.startswith('+44'):
            return "Only +44 numbers allowed!", 400

        existing_user = User.query.filter_by(phone_number=phone).first()
        if existing_user:
            return "User already registered. Please log in instead."

        new_user = User(phone_number=phone, terms_accepted=True)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return redirect(url_for('dashboard'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form.get('phone_number')
        user = User.query.filter_by(phone_number=phone).first()
        if not user:
            return "User not found. Please register first."

        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))