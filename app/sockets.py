from flask_socketio import join_room, leave_room
from flask import request
from . import rooms, users

def register_socket_events(socketio):
    @socketio.on("connect")
    def on_connect():
        print("Client connected")

    @socketio.on("disconnect")
    def on_disconnect():
        print("Client disconnected")

    @socketio.on("join_room")
    def on_join(data):
        room_id = int(data.get("room_id"))
        user = data.get("user")
        join_room(room_id)

        if room_id in rooms.keys():
            if user not in rooms[room_id].currentUsers:
                rooms[room_id].currentUsers.append(user)
        else:
            print(f"Room {room_id} not found")

        print(f"{user} joined room {room_id}")
        socketio.emit("user_joined", {"user": user}, room=room_id)

    @socketio.on("leave_room")
    def on_leave(data):
        room_id = int(data.get("room_id"))
        user = data.get("user")
        leave_room(room_id)

        if room_id in rooms.keys():
            if user in rooms[room_id].currentUsers:
                rooms[room_id].currentUsers.remove(user)
            if len(rooms[room_id].currentUsers) == 0:
                del rooms[room_id]
                print(f"Room {room_id} deleted due to no user")
        else:
            print(f"Room {room_id} not found")
            
        print(f"{user} left room {room_id}")
        socketio.emit("user_left", {"user": user}, room=room_id)


    @socketio.on("send_message")
    def on_message(data):
        room_id = int(data.get("room_id"))
        message_type = data.get("message_type")
        print(f"sent {message_type} from {room_id}")

        match message_type:
            case "msg":
                message = data.get("message")
                socketio.emit("receive_message", {"message": message}, room=room_id)
            case "play":
                socketio.emit("broadcast_play", {}, room=room_id, include_self=False)
            case "pause":
                socketio.emit("broadcast_pause", {}, room=room_id, include_self=False)
            case "ping":
                socketio.emit("pong", {}, to=request.sid)
            case _:
                print("Wrong control signal")
