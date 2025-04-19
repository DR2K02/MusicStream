from flask import Flask
from flask_cors import CORS
from .database import db 
from . import mail_flask
from flask_jwt_extended import JWTManager

from werkzeug.security import generate_password_hash
from .cache import cache
#from werkzeug.urls import url_quote_plus

DB_Name="musica.sqlite"

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='secret_key'
    app.config['JWT_SECRET_KEY']='jwt_secret'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_Name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
    app.config['JWT_BLACKLIST_ENABLED']=True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access']

    db.init_app(app)
    CORS(app)

# ----------Cache Implementation------------
    cache.init_app(app)

# ----------Configuring mail----------------
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT']=465
    app.config['MAIL_USERNAME']='amarbose1897@gmail.com'
    app.config['MAIL_PASSWORD']='gjibossejtktbjtg'
    app.config['MAIL_USE_TLS']=False
    app.config['MAIL_USE_SSL']=True

    mail_flask.mail.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api_bp

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(api_bp,url_prefix='/')

    #--------------JWT Implemetation----------
    from .models import User 
    jwt=JWTManager(app)
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header,jwt_data):
        identity=jwt_data["sub"]
        return User.query.filter_by(user_id=identity).one_or_none()
    #------------Database Implemetation-----------
    with app.app_context():
        db.create_all()
        user=User.query.filter_by(email='dipanjan2002aein@gmail.com').first()
        if user:
            pass
        else:
            first_user=User(email='dipanjan2002aein@gmail.com',name='Dipanjan Rout',password=generate_password_hash('password',method='scrypt'),is_admin=True)
            db.session.add(first_user)
            db.session.commit()
    
    app.app_context().push()

    return app