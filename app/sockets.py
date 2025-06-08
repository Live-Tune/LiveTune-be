from flask_socketio import join_room, leave_room
from flask import request
from . import rooms, users, sid_user_map
from app.utils import find_room

def register_socket_events(socketio):
    @socketio.on("connect")
    def on_connect():
        print(f"Client connected: {request.sid}")

    @socketio.on("disconnect")
    def on_disconnect():
        print(f"Client disconnected: {request.sid}")
        user_id = sid_user_map.pop(request.sid, None) # remove SID and get associated user_id

        if user_id:
            print(f"User {user_id} (SID: {request.sid}) disconnected. Cleaning up their rooms.")
            
            for room_id_key in list(rooms.keys()): # iterate over a copy of room IDs as rooms dictionary might be modified
                room = find_room(rooms, room_id_key)
                if room and user_id in room.current_users:
                    room.remove_user(user_id)
                    print(f"User {user_id} removed from room {room_id_key} due to disconnect.")
                    socketio.emit("user_left", {"user": user_id, "room_id": room_id_key}, room=room_id_key)
                    
                    if not room.current_users: # If room becomes empty
                        del rooms[room_id_key]
                        print(f"Room {room_id_key} deleted as it became empty.")
        else:
            print(f"SID {request.sid} disconnected, no user mapping found or already cleaned up.")

    @socketio.on("join_room")
    def on_join(data):
        room_id = int(data.get("room_id"))
        user = data.get("user")
        join_room(room_id)

        sid_user_map[request.sid] = user

        if find_room(rooms, room_id) != None:
            if user not in rooms[room_id].current_users:
                rooms[room_id].add_user(user)
        else:
            print(f"Room {room_id} not found")

        print(f"{user} joined room {room_id}")
        socketio.emit("user_joined", {"user": user}, room=room_id)

    @socketio.on("leave_room")
    def on_leave(data):
        room_id = int(data.get("room_id"))
        user = data.get("user") # we could replace this for user = sid_user_map.get(request.sid)
        leave_room(room_id)

        if find_room(rooms, room_id) != None:
            if user in rooms[room_id].current_users:
                rooms[room_id].remove_user(user)
            if len(rooms[room_id].current_users) == 0:
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
