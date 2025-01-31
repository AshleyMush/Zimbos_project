from flask import Blueprint

website_bp = Blueprint(
    'website_bp',
    __name__,
    template_folder='templates',
    static_folder='static',
)

from . import routes  # Import routes after creating the blueprint