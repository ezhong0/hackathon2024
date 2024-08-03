from flask import Flask
# from flask_migrate import Migrate # uncomment if need
# from flask_session import Session # uncomment if need

# from .models.db import db # uncomment if need
from .settings import APP_SETTINGS

# migrate = Migrate() # uncomment if need 
# session = Session() # uncomment if need 

def create_app():
    app = Flask(__name__)
    app.config.update(APP_SETTINGS)

    # db.init_app(app) # uncomment is need 
    # migrate.init_app(app, db) # uncomment if need 

    # session.init_app(app) # uncomment is need 
    return app
