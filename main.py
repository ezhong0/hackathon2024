from app import socketio, app

# socketio = SocketIO(app, async_mode='eventlet')

if __name__ == '__main__':
    print("Starting the Flask application...")
    socketio.run(app, host='0.0.0.0', port=5001)
    print("Starting the Flask application...1")
