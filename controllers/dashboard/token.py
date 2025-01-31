from flask import Blueprint, render_template, request, redirect, url_for, session, abort
from models import db, User
from . import dashboard_bp
from models import User, Group, GroupToken
from datetime import datetime, timedelta





@dashboard_bp.route('/use_token/<token>', methods=['GET'])
def use_token(token):
    group_token = GroupToken.query.filter_by(token=token).first()

    if not group_token:
        abort(404, "Invalid token")

    if group_token.used:
        abort(400, "Token already used")
    if group_token.expires_at < datetime.utcnow():
        abort(400, "Token expired")

    # Mark token as used
    group_token.used = True
    db.session.commit()

    # Increment user's joined count
    user = User.query.get(group_token.user_id)
    user.groups_joined_count += 1
    db.session.commit()

    # Redirect to the actual WhatsApp invite link
    return redirect(group_token.group.whatsapp_link)
