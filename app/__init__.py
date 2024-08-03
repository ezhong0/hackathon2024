from flask import Flask
# from flask_migrate import Migrate # uncomment if need
# from flask_session import Session # uncomment if need
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from .models.db import db # uncomment if need
from .settings import APP_SETTINGS

# migrate = Migrate() # uncomment if need 
# session = Session() # uncomment if need 

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config) 

    db = SQLAlchemy(app)
    migrate = Migrate(app,db)
    # db.init_app(app) # uncomment is need 
    # migrate.init_app(app, db) # uncomment if need 

    # session.init_app(app) # uncomment is need 

    with app.app_context():
        # Import and register routes
        from . import routes
    
    return app
