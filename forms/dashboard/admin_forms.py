from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class AddGroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    group_link = StringField('Group Link', validators=[DataRequired(), URL()])
    submit = SubmitField('Add Group')
