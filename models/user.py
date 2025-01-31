from flask_login import UserMixin
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, Integer
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    groups_joined_count = db.Column(db.Integer, default=0)
    # For GDPR compliance, record whether the user has accepted T&Cs and cookies.
    terms_accepted = db.Column(db.Boolean, default=False)
    cookie_consent = db.Column(db.Boolean, default=False)