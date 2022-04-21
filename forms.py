
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo

#Account registration
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

#login page
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    admin = BooleanField('Admin login')
    submit = SubmitField('Login')

#Account personal information
class InformationForm(FlaskForm):
    Fullname = StringField('fullname',validators=[DataRequired()])
    location = RadioField('location',
        choices=[('online','online'),('onsite','onsite service')],
        validators=[DataRequired()])
    skills = StringField('Name of skill to be provided',validators=[DataRequired()])
    website = StringField('Website/portfolio link')
    email = StringField('Email for contact',validators=[DataRequired(), Email()])
    phone = StringField('Phone number',validators=[DataRequired(), Length(min=8, max=8)])
    experience = StringField('Years of experience',validators=[DataRequired(), Length(min=1, max=2)])
    selfintro = StringField('Simple self introduction',validators=[Length(max=250)])
    submit = SubmitField('submit')

#Search
class Search(FlaskForm):
    Keyword = StringField('',validators=[DataRequired()])
    submit = SubmitField('submit')

#Contact freelancer
class EmailForm(FlaskForm):
    name =StringField('name',validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email for contact',validators=[DataRequired(), Email()])    
    submit = SubmitField('submit')

#Password Change
class PasswordForm(FlaskForm):
    oldpassword = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')