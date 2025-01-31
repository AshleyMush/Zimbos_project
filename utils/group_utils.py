from models import User, Group, GroupToken
from datetime import datetime, timedelta
import uuid
from models import db




def generate_single_use_token(user_id, group_id):
    token_str = str(uuid.uuid4())
    token = GroupToken(
        token=token_str,
        user_id=user_id,
        group_id=group_id,
        used=False,
        expires_at=datetime.utcnow() + timedelta(hours=24)  # Token valid for 24h
    )
    db.session.add(token)
    db.session.commit()
    return token.token


def user_can_join_more_groups(user):
    return user.groups_joined_count < 3

