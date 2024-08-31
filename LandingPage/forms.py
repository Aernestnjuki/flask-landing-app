from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, IntegerField, SubmitField, FloatField, BooleanField,\
    TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired


class SignUpForm(FlaskForm):
    email = EmailField('Enter your email', validators=[DataRequired()])
    username = StringField('Enter your name', validators=[DataRequired(), Length(min=2)])
    password1 = PasswordField('Enter password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Enter your email', validators=[DataRequired()])
    password = PasswordField('Enter password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')


class AddProjectForm(FlaskForm):
    title = StringField('Project title', validators=[DataRequired()])
    location = StringField('project location', validators=[DataRequired()])
    price = FloatField('Project price', validators=[DataRequired()])
    project_image = FileField('Project image', validators=[FileRequired()])
    project_video = FileField('Project Video', validators=[FileRequired()])
    about_project = TextAreaField('Enter more information about the project')
    display_project = BooleanField('Display project')
    add_project = SubmitField('Add Project')
    update_project = SubmitField('Update')


class BlogForm(FlaskForm):
    blog_title = StringField('Blog Title', validators=[DataRequired()])
    blog_image = FileField('Blog Image', validators=[FileRequired()])
    blog_content = TextAreaField('Blog Content')
    display_blog = BooleanField('Publish Blog')
    add_blog = SubmitField('Add Blog')
    update_blog = SubmitField('Update Blog')


class ClientInfo(FlaskForm):
    client_name = StringField('Enter name', validators=[DataRequired(), Length(min=4)])
    phone_number = IntegerField('Phone number', validators=[DataRequired()])
    land_location = StringField('Land location', validators=[DataRequired()])
    budget = StringField('Your budget', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EmailForm(FlaskForm):
    username = StringField('Enter your Name', validators=[DataRequired(), Length(min=2)])
    email = EmailField('Enter your Email', validators=[DataRequired()])
    subject = StringField('Enter Subject', validators=[DataRequired()])
    message = TextAreaField('Enter email message')
    submit = SubmitField('Send Email')