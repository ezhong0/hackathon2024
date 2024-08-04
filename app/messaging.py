from flask_socketio import SocketIO, join_room, send
from flask import session
from app import socketio

@socketio.on('private_message')
def handle_private_message(data):
    sender_id = str(session.get('user_id'))  # Convert sender_id to string
    recipient_id = str(data['recipient_id'])  # Convert recipient_id to string
    message = data['message']
    
    print(f'Received message from {sender_id} to {recipient_id}: {message}')

    # Use strings for comparison
    #room = f'private_{min(sender_id, recipient_id)}_{max(sender_id, recipient_id)}'
    room = "room"
    print(f'{room}')
    send({'msg': message, 'sender': sender_id}, room=room)

@socketio.on('join_private')
def on_join(data):
    sender_id = session.get('user_id')
    recipient_id = data['recipient_id']
    
    #room = f'private_{min(str(sender_id), str(recipient_id))}_{max(str(sender_id), str(recipient_id))}'
    room = "room"

    join_room(room)
    print(f'User {sender_id} joined room: {room}')