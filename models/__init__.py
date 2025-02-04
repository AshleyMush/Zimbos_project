from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.group import Group
from models.token import Token
