from models import db
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, Integer

from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"  # Changed to lowercase
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), nullable=False)
    email: Mapped[str] = mapped_column(db.String(2000), nullable=False)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    country: Mapped[str] = mapped_column(db.String(50), nullable=True)
    password: Mapped[str] = mapped_column(db.String(2000), nullable=True)
    sex: Mapped[str] = mapped_column(db.String(10), nullable=True)
    is_admin: Mapped[bool] = mapped_column(db.Boolean, default=False)
    role: Mapped[str] = mapped_column(String(1000), nullable=False, default='User')
    groups_joined_count: Mapped[int] = mapped_column(db.Integer, default=0)

    tokens: Mapped[list["Token"]] = relationship(
        "Token",
        backref="user",
        cascade="all, delete-orphan",

    )

    def __repr__(self):
        return f'<User {self.email}>'

