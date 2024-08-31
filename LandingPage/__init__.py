from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
DB_NAME = 'LandingBD.db'
MAIL = Mail()


def create_database():
    db.create_all()
    print('Database created')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'aernestnjuki@gmail.com'
    app.config['MAIL_PASSWORD'] = 'kjrd ueml oxqw wbrp'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    db.init_app(app)
    MAIL.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def user_loader(id):
        return Register.query.get(int(id))

    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Register, LoadProject, CreateBlog, CustomerInformation

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # with app.app_context():
    #     create_database()

    return app