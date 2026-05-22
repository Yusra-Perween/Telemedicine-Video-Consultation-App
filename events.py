from extensions import socketio
from flask_socketio import emit, join_room

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    # Notify others in the room that someone joined
    emit('ready', {'msg': 'User joined'}, to=room, include_self=False)

@socketio.on('offer')
def on_offer(data):
    emit('offer', data, to=data['room'], include_self=False)

@socketio.on('answer')
def on_answer(data):
    emit('answer', data, to=data['room'], include_self=False)

@socketio.on('ice_candidate')
def on_ice_candidate(data):
    emit('ice_candidate', data, to=data['room'], include_self=False)
