# REST API endpoints

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

    name = data.get('room_name')
    is_private = data.get('is_room_private', False)
    description = data.get('room_description')
    max_user = data.get('room_maxUser')
    host = data.get('room_host')
   
    rooms[next_room_id] = Room(name=name, isPrivate=is_private, description=description, maxUser=max_user, host=host, ID=next_room_id)
    next_room_id += 1

    return "Room created successfully.", 201


# Update room settings
@app.route("/api/room/updatesettings", methods=["PUT"])
def updatesettings():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    name = data.get('name')
    description = data.get('description')
    max_user = data.get('max_user')
    host = data.get('host')
    id = data.get('id')

    rooms[id].update_settings(name, description, max_user, host)

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
    id = data.get('id')

    if id in rooms:
        del rooms[id]
        return "Room deleted successfully.", 200
    else:
        return "Room not found.", 404

# Retrieving ID from room name
@app.route('/api/room/getid', methods=['GET']) 
def get_room_id():           
    name = request.args.get('name')
    for room_id, room_obj in rooms.items():
        if room_obj.name == name:
            return jsonify({"id": room_id})
    
    return jsonify({"error": "Room not found"}), 404

# Retrieve room info
@app.route('/api/room/info', methods=['GET'])
def get_room_info():
    
    try:
        id = int(request.args.get('id'))
    except ValueError:
        return jsonify({"error": "The ID must be a number"}), 400

    room = rooms[id]
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
        id = int(request.args.get('id'))
    except ValueError:
        return jsonify({"error": "The ID must be a number"}), 400

    room = rooms[id]
    room_data = room.to_dict()
    if room_data:
        return jsonify(room_data.get("queue")), 200
    else:
        return jsonify({"error": "Room not found"}), 404

# TEST  
if __name__ == "__main__":
    app.run(debug=True, port=5000)