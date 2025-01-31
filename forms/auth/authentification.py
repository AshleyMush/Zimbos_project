from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Regexp

class RegisterForm(FlaskForm):
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(),
            Regexp(r'^\+44', message="Must start with +44"),
        ]
    )
    accept_terms = BooleanField(
        'I agree to the Terms and Conditions',
        validators=[DataRequired()]
    )
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Login')
