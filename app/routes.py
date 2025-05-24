# REST API endpoints
import os
from flask import Flask, request, jsonify
from classes import Room

rooms = {}
users = {}

next_room_id = 1
# ID is just a counter now

app = Flask(__name__)

## -- ROOMS -- 

# Create room
@app.route("/api/room/createnew", methods=["POST"])
def createroom():
    
    global next_room_id

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    room_name = data.get('room_name')
    is_room_private = data.get('is_room_private', False)
    room_description = data.get('room_description')
    room_maxUser = data.get('room_maxUser')
    room_host = data.get('room_host')
   
    rooms[next_room_id] = Room(name=room_name, isPrivate=is_room_private, description=room_description, maxUser=room_maxUser, host=room_host, ID=next_room_id)
    next_room_id += 1

    return "Room created successfully.", 201


# Update room settings
@app.route("/api/room/updatesettings", methods=["PUT"])
def updatesettings():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    new_room_name = data.get('new_room_name')
    new_room_description = data.get('new_room_description')
    new_room_maxUser = data.get('new_room_maxUser')
    new_room_host = data.get('new_room_host')
    room_id = data.get('room_id')

    rooms[room_id].update_settings(new_room_name, new_room_description, new_room_maxUser, new_room_host)

    return "Room updated successfully.", 201

# Retrieve available public rooms
@app.route("/api/room/availablepublicrooms", methods=["GET"])
def getpublicrooms():

    public_rooms_data = []
    for room_id, room_obj in rooms.items():
        if not room_obj.isPrivate:
            # 일단 I will return the whole object but I think we should
            # only return a couple properties
            public_rooms_data.append(room_obj.to_dict())

    return jsonify(public_rooms_data), 200

# Deleting a room
@app.route("/api/room/deleteroom", methods=["DELETE"])
def deleteroom():

    data = request.get_json()
    delete_room_id = data.get('delete_room_id')

    if delete_room_id in rooms:
        del rooms[delete_room_id]
        return "Room deleted successfully.", 200
    else:
        return "Room not found.", 404

# Retrieving ID from room name
@app.route('/api/room/getid', methods=['GET']) 
def get_room_id():           
    query_room_name = request.args.get('name')
    for room_id, room_obj in rooms.items():
        if room_obj.name == query_room_name:
            return jsonify({"id": room_id})
    
    return jsonify({"error": "Room not found"}), 404

# Retrieve room info
@app.route('/api/room/info', methods=['GET'])
def get_room_info():
    
    try:
        room_id = int(request.args.get('id'))
    except ValueError:
        return jsonify({"error": "The ID must be a number"}), 400

    room = rooms[room_id]
    room_data = room.to_dict()
    if room_data:
        filtered = {
            "room_name": room_data["name"],
            "description": room_data["description"],
            "current_users_number": len(room_data.get("currentUsers")),
            "host": room_data["host"],
        }
        return jsonify(filtered), 200
    else:
        return jsonify({"error": "Room not found"}), 404
    
@app.route('/api/room/songlist', methods=['GET'])
def get_song_list():

    try:
        room_id = int(request.args.get('id'))
    except ValueError:
        return jsonify({"error": "The ID must be a number"}), 400

    room = rooms[room_id]
    room_data = room.to_dict()
    if room_data:
        return jsonify(room_data.get("queue")), 200
    else:
        return jsonify({"error": "Room not found"}), 404

# TEST  
if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "production") == "development"

    app.run(host=host, port=port, debug=debug)