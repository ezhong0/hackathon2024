from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = DecimalField('Age ', validators=[DataRequired()])
    field = StringField('Field', validators=[DataRequired()])
    location = StringField('Location')
    selfDescription = StringField('Self-Description',validators=[DataRequired()])
    experience = StringField('Experience')
    strength = StringField('Strengths/Skills')
    goals = StringField('Aspirations')
    submit = SubmitField('Create Account')