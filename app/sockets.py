from flask_socketio import join_room, leave_room
from flask import request
from . import rooms, users
from app.utils import find_room

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
        uid = data.get("uid")
        join_room(room_id)

        if find_room(rooms, room_id) != None:
            if uid not in rooms[room_id].current_users:
                rooms[room_id].current_users.append(uid)
        else:
            print(f"Room {room_id} not found")

        print(f"{users[uid].username} joined room {room_id}")
        socketio.emit("user_joined", {"uid": uid}, room=room_id)

    @socketio.on("leave_room")
    def on_leave(data):
        room_id = int(data.get("room_id"))
        uid = data.get("uid")
        leave_room(room_id)

        if find_room(rooms, room_id) != None:
            if uid in rooms[room_id].current_users:
                rooms[room_id].current_users.remove(uid)
            if len(rooms[room_id].current_users) == 0:
                del rooms[room_id]
                print(f"Room {room_id} deleted due to no user")
        else:
            print(f"Room {room_id} not found")
            
        print(f"{users[uid].username} left room {room_id}")
        socketio.emit("user_left", {"uid": uid}, room=room_id)


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
