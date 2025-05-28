from flask_socketio import join_room
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
        room_id = data.get("room_id")
        user = data.get("user")
        join_room(room_id)

        if room_id in rooms:
            print("id in room")
            room = rooms[room_id]
            if user not in room.currentUsers:
                room.currentUsers.append(user)

        print(f"{user} joined room {room_id}")
        socketio.emit("user_joined", {"user": user}, room=room_id)

    @socketio.on("leave_room")
    def on_leave(data):
        room_id = data.get("room_id")
        user = data.get("user")
        leave_room(room_id)

        if room_id in rooms:
            room = rooms[room_id]
            if user in room.currentUsers:
                room.currentUsers.remove(user)
                print(f"{user} removed from room {room_id}")
        else:
            print(f"Room {room_id} not found")

        socketio.emit("user_left", {"user": user}, room=room_id)


    @socketio.on("send_message")
    def on_message(data):
        room_id = data.get("room_id")
        message_type = data.get("message_type")
        print(f"sent {message_type} in {room_id}")

        match message_type:
            case "msg":
                message = data.get("message")
                socketio.emit("receive_message", {"message": message}, room=room_id)
            case "play":
                socketio.emit("broadcast_play", {}, room=room_id)
            case "stop":
                socketio.emit("broadcast_stop", {}, room=room_id)
            case _:
                print("Wrong control signal")
