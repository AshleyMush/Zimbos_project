from models import db
from sqlalchemy.orm import Mapped, mapped_column



class Group(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    group_name : Mapped[str] = mapped_column(db.String(50), nullable=False)
    group_link : Mapped[str] = mapped_column(db.String(2000), nullable=False)

    def __repr__(self):
        return f'<Group {self.group_name}>'
