from flask import Flask, render_template, request, redirect, url_for, session, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid
from models import db
from models import User, Group, GroupToken
from flask_ckeditor import CKEditor
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_manager
from controllers.auth import auth_bp
from controllers.dashboard import dashboard_bp
from controllers.website import website_bp




app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'  # Replace with something secure
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whatsapp_mvp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ckeditor = CKEditor(app)
Bootstrap5(app)
csrf = CSRFProtect(app)
db.init_app(app)




# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)



# Register Blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(website_bp)



# ---------------------- #
#     HELPER FUNCTIONS   #
# ---------------------- #







@app.route('/setup')
def setup():
    db.drop_all()
    db.create_all()

    # Add sample groups
    sample_groups = [
        Group(name="Zim Group 1", whatsapp_link="https://chat.whatsapp.com/invite_link_for_group_1"),
        Group(name="Zim Group 2", whatsapp_link="https://chat.whatsapp.com/invite_link_for_group_2"),
        Group(name="Zim Group 3", whatsapp_link="https://chat.whatsapp.com/invite_link_for_group_3"),
        Group(name="Zim Group 4", whatsapp_link="https://chat.whatsapp.com/invite_link_for_group_4"),
    ]
    db.session.add_all(sample_groups)
    db.session.commit()

    return "Database setup complete!"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
