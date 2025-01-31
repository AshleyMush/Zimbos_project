from flask import Blueprint, render_template, request, make_response, redirect, url_for
from flask_login import current_user
from models import db
from . import website_bp







@website_bp.route('/')
def index():
    # Check if we already have cookie consent from the user (via a cookie in the browser).
    cookie_consent = request.cookies.get('cookie_consent', 'false') == 'true'
    return render_template('index.html', cookie_consent=cookie_consent)


@website_bp.route('/cookie_consent', methods=['POST'])
def cookie_consent():
    """
    When a user clicks "I agree" on the cookie banner,
    set a cookie and optionally store in the database if the user is logged in.
    """
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('cookie_consent', 'true', max_age=365 * 24 * 60 * 60)  # 1 year
    user = current_user
    if user:
        user.cookie_consent = True
        db.session.commit()
    return resp

