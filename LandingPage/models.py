from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('You should not read these password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f'Username: {self.username} and Email: {self.email} created!'


class LoadProject(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    project_image = db.Column(db.String(500), nullable=False)
    project_video = db.Column(db.String(500), nullable=False)
    about_project = db.Column(db.Text, nullable=False)
    display_project = db.Column(db.Boolean, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'Project title: {self.title} and Project image: {self.project_image} created!'


class CreateBlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(200), nullable=False)
    blog_image = db.Column(db.String(300), nullable=False)
    blog_content = db.Column(db.String(1000000), nullable=False)
    display_blog = db.Column(db.Boolean, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.blog_title} has been created'


class CustomerInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.Integer(), nullable=False, unique=True)
    land_location = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

