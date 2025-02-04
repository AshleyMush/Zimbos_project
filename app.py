import os
import logging
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.user import User
from controllers.auth import auth_bp
from controllers.dashboard import dashboard_bp

# Initialize Flask application
app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Define the base directory and ensure the instance folder exists
BASEDIR = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(BASEDIR, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Configure the application
app.config['SECRET_KEY'] = os.environ.get("SECRET_APP_KEY", "default_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URI", f"sqlite:///{os.path.join(instance_path, 'Zimbos.db')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
Bootstrap5(app)
csrf = CSRFProtect(app)
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # This should match your login route endpoint

@login_manager.user_loader
def load_user(user_id):
    # Use db.session.get() or User.query.get() depending on your SQLAlchemy version
    return db.session.get(User, int(user_id))

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# Create database tables (if they do not already exist)
with app.app_context():
    try:
        db.create_all()
    except SQLAlchemyError as e:
        app.logger.error(f"Error creating tables: {e}")
        db.session.rollback()

# 404 Error Handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, port=5002)
