from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate
import signal
import sys
import os
import eventlet

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app, async_mode='eventlet')
#socketio.run(app, host='0.0.0.0', port=5001)

from app import routes, models

# Signal handler for logging out all users
def signal_handler(sig, frame):
    print("\nLogging out all users...")
    app.secret_key = os.urandom(24)  # Change secret key to invalidate sessions
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)