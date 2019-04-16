from flask_socketio import SocketIO

socketio = SocketIO()


@socketio.on('connect')
def connect():
    pass

@socketio.on('disconnect')
def disconnect():
    pass
