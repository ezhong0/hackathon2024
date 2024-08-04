from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Sign Up')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = DecimalField('Age', validators=[DataRequired()], places=0)  # Use places=0 to ensure it's an integer
    field = StringField('Field', validators=[DataRequired()])
    location = StringField('Location')
    self_description = StringField('Self-Description', validators=[DataRequired()])  # Changed to match the original field name
    experience = StringField('Experience')
    strength = StringField('Strengths/Skills')
    goals = StringField('Aspirations')
    submit = SubmitField('Create Account')
<<<<<<< HEAD

class PreferencesForm(FlaskForm):
    pAge = IntegerField('Preferred Age', validators=[DataRequired()])
    pField = StringField('Preferred Field', validators=[DataRequired()])
    pLocation = StringField('Preferred Location', validators=[DataRequired()])
    pGoals = StringField('Preferred Goals', validators=[DataRequired()])
    pQualities = StringField('Preferred Qualities', validators=[DataRequired()])
    submit = SubmitField('Update Preferences')
=======
    profile_photo = FileField('Profile Photo', validators=[FileRequired()])
>>>>>>> 74f780b6c9b732eb1003c3c121f8da8a0013f411
