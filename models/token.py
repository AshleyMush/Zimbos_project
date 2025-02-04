from models import db
import uuid
from sqlalchemy.orm import Mapped, mapped_column



class Token(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    token : Mapped[str] = mapped_column(db.String(2000), default=uuid.uuid4, nullable=False )
    user_id : Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id : Mapped[int] = mapped_column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    used : Mapped[bool] = mapped_column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Token {self.token} for user {self.user_id}>'
