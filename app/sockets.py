from flask_socketio import join_room, leave_room
from flask import request
from . import rooms, users
from app.utils import find_room

sid_map = {}
uid_map = {}

def register_socket_events(socketio):
    @socketio.on("connect")
    def on_connect():
        print(f"Client connected: sid={request.sid}")

    @socketio.on("disconnect")
    def on_disconnect():
        print(f"Client disconnected: {request.sid}")
        uid = uid_map.pop(request.sid, None)
        sid = sid_map.pop(uid, None)

        if uid:
            print(f"User {uid} (SID: {request.sid}) disconnected. Cleaning up their rooms.")

            for room_id_key in list(rooms.keys()):
                room = find_room(rooms, room_id_key)
                if room and uid in room.current_users:
                    room.remove_user(uid)
                    print(f"User {uid} removed from room {room_id_key} due to disconnect.")
                    socketio.emit("user_left", {"uid": uid}, room=room_id_key)

                    if len(room.current_users) == 0:
                        del rooms[room_id_key]
                        print(f"Room {room_id_key} deleted as it became empty.")
        else:
            print(f"SID {request.sid} disconnected, no user mapping found or already cleaned up.")

    @socketio.on("join_room")
    def on_join(data):
        room_id = int(data.get("room_id"))
        uid = data.get("uid")
        sid_map[uid] = request.sid
        uid_map[request.sid] = uid
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
        del sid_map[uid]
        del uid_map[request.sid]
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
            case "sync":
                timestamp = data.get("timestamp");
                socketio.emit("broadcast_sync", {"timestamp": timestamp}, room=room_id, include_self=False)
            case "req_sync":
                host_uid = rooms[room_id].host
                host_sid = sid_map[host_uid]
                socketio.emit("req_sync", {}, to=host_sid)
            case "add":
                video = data.get("video")
                rooms[room_id].queue.append(video)
                socketio.emit("broadcast_add", {"video": video}, room=room_id, include_self=False)
            case "skip":
                print(rooms[room_id].queue[0])
                rooms[room_id].current_song = rooms[room_id].queue[0]
                print(rooms[room_id].current_song)
                rooms[room_id].queue.pop(0)
                socketio.emit("broadcast_skip", {}, room=room_id, include_self=False)
            case "ping":
                socketio.emit("pong", {}, to=request.sid)
            case _:
                print("Wrong control signal")
