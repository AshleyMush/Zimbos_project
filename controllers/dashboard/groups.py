from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from models import db, User, Group, GroupToken
from . import dashboard_bp
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from utils.group_utils import user_can_join_more_groups, generate_single_use_token





@dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    Shows the user:
    - Their current group joins (max 3)
    - The single-use tokens they've generated (and not used)
    - A search bar to find groups
    """
    user = current_user
    if not user:
        return redirect(url_for('login'))

    # If user hasn't accepted T&C, force them to accept T&C
    if not user.terms_accepted:
        return redirect(url_for('auth_bp.terms'))

    search_query = request.args.get('search', '')

    # Basic group search by name
    if search_query:
        groups = Group.query.filter(Group.name.ilike(f"%{search_query}%")).all()
    else:
        groups = Group.query.all()

    # Tokens the user has that are still valid and not used
    active_tokens = GroupToken.query.filter(
        GroupToken.user_id == user.id,
        GroupToken.used == False,
        GroupToken.expires_at > datetime.utcnow()
    ).all()

    return render_template(
        'dashboard.html',
        user=user,
        groups=groups,
        search_query=search_query,
        active_tokens=active_tokens
    )


@dashboard_bp.route('/request_group/<int:group_id>', methods=['POST'])
def request_group(group_id):
    user = current_user
    if not user:
        return redirect(url_for('login'))

    group = Group.query.get(group_id)
    if not group:
        abort(404, "Group not found")

    # Check if user can still join more groups
    if not user_can_join_more_groups(user):
        return "You have reached the maximum number of groups allowed (3).", 403

    # Generate a single-use token
    token_str = generate_single_use_token(user.id, group.id)
    return redirect(url_for('dashboard'))

