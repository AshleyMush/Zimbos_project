from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email

# A sample list of country choices (extend as needed)
COUNTRY_CHOICES = [
    ('ZW', 'Zimbabwe'),
    ('UK', 'United Kingdom'),
    ('US', 'United States'),
    ('CA', 'Canada'),
    ('AU', 'Australia'),
    ('IN', 'India'),
    ('BR', 'Brazil'),
    ('DE', 'Germany'),
    ('RU', 'Russia'),
    ('FR', 'France'),
    ('JP', 'Japan'),
    ('CN', 'China'),
    ('KR', 'South Korea'),
    ('SA', 'South Africa'),
    ('NG', 'Nigeria'),
    ('KE', 'Kenya'),
    ('TZ', 'Tanzania'),
    ('UG', 'Uganda'),
    ('GH', 'Ghana'),
    ('EG', 'Egypt'),
    ('AE', 'United Arab Emirates'),
    ('SA', 'Saudi Arabia'),
    ('QA', 'Qatar'),
    ('KW', 'Kuwait'),
    ('OM', 'Oman'),
    ('BH', 'Bahrain'),
    ('JO', 'Jordan'),
    ('LB', 'Lebanon'),
    ('SY', 'Syria'),
    ('IQ', 'Iraq'),
    ('IR', 'Iran'),
    ('AF', 'Afghanistan'),
    ('PK', 'Pakistan'),
    ('BD', 'Bangladesh'),
    ('NP', 'Nepal'),
    ('LK', 'Sri Lanka'),
    ('MM', 'Myanmar'),
    ('TH', 'Thailand'),
    ('VN', 'Vietnam'),
    ('PH', 'Philippines'),
    ('ID', 'Indonesia'),
    ('MY', 'Malaysia'),
    ('SG', 'Singapore'),
    ('KH', 'Cambodia'),
    ('LA', 'Laos')
    # Add more countries here
]

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    country = SelectField('Country', choices=COUNTRY_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')
