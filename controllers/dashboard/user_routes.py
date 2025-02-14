from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from models.user import User
from models.token import Token
from models.group import Group
from models import db
from forms import SearchForm
from . import dashboard_bp
from flask_login import current_user, login_required


# You can also import helper functions from utils if needed



@dashboard_bp.route('/user-dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    user = current_user
    form = SearchForm()
    tokens = Token.query.filter_by(user_id=user.id).all()
    groups = None

    if form.validate_on_submit():
        groups = Group.query.filter(
            Group.group_name.ilike(f"%{form.search_query.data}%")
        ).all()

    return render_template(
        'dashboard/user-dashboard.html',
        user=user,
        form=form,
        tokens=tokens,
        groups=groups
    )


@dashboard_bp.route('/generate_token/<int:group_id>')
@login_required
def generate_token_route(group_id):
    token_count = Token.query.filter_by(user_id=current_user.id, used=False).count()
    if token_count >= 3:
        flash('You have reached the maximum number of active tokens (3).', 'danger')
        return redirect(url_for('dashboard_bp.user_dashboard'))

    new_token = Token(user_id=current_user.id, group_id=group_id)
    db.session.add(new_token)
    db.session.commit()
    flash('Token generated successfully! Use it to join the group.', 'success')
    return redirect(url_for('dashboard_bp.user_dashboard'))

@dashboard_bp.route('/use_token/<token>')
@login_required
def use_token(token):


    token_obj = Token.query.filter_by(token=token, user_id=current_user.id, used=False).first()
    if not token_obj:
        flash('Invalid or already used token.', 'danger')
        return redirect(url_for('dashboard_bp.user_dashboard'))

    # Mark token as used so it cannot be reused
    token_obj.used = True
    db.session.commit()

    # Retrieve the group link and redirect the user
    group = Group.query.get(token_obj.group_id)
    if group:
        flash('Token used successfully. Redirecting to group link.', 'success')
        return redirect(group.group_link)
    else:
        flash('Group not found', 'danger')
        return redirect(url_for('dashboard_bp.user_dashboard'))
