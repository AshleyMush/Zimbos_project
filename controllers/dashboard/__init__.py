from flask import Blueprint

dashboard_bp = Blueprint(
    'dashboard_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/dashboard'

)

from .user_routes import *
from .admin_routes import *
