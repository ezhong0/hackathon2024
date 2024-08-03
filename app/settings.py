import datetime

APP_SETTINGS = {
    "SECRET_KEY": "YOUR_SECRET_KEY_HERE",
    # "SQLALCHEMY_DATABASE_URI": "sqlite:///master.sqlite3", # uncomment this line if need 
    "PERMANENT_SESSION_LIFETIME": datetime.timedelta(days=7),
    # "SESSION_PERMANENT": False, # uncomment this line if need 
    # "SESSION_TYPE": "filesystem", # uncomment this line if need 
}

TIMEZONE = datetime.timezone.utc
DEBUG = True
