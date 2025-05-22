# REST API endpoints

from flask import Flask, request, jsonify
from classes import Room

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
    room_id = len(rooms) + 1
   
    rooms[next_room_id] = Room(name=room_name, isprivate=is_room_private, description=room_description, maxUser=room_maxUser, host=room_host, ID=next_room_id)
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
        if not room_obj.isprivate:
            # 일단 I will return the whole object but I think we should
            # only return a couple properties
            public_rooms_data.append(room_obj.to_dict())

    return jsonify(public_rooms_data), 200

@app.route("/api/room/deleteroom", methods=["DELETE"])
def deleteroom():

    data = request.get_json()
    delete_room_id = data.get('delete_room_id')

    if delete_room_id in rooms:
        del rooms[delete_room_id]
        return "Room deleted successfully.", 200
    else:
        return "Room not found.", 404

@app.route('/api/room/getid', methods=['GET']) 
def get_room_id():           
    room_title = request.args.get('title')
    for room_id, room_data in rooms.items():
        if room_data.get("title") == room_title:
            return jsonify({"id": room_id})
    
    return jsonify({"error": "Room not found"}), 404
    
@app.route('/api/room/info', methods=['GET'])
def get_room_info():
    room_id = request.args.get('id')
    room = rooms.get(room_id)
    if room:
        filtered = {
            "title": room.get("title"),
            "description": room.get("description"),
            "currentUsers": room.get("currentUsers")
        }
        return jsonify(filtered)
    else:
        return jsonify({"error": "Room not found"}), 404
    
@app.route('/api/room/songlist', methods=['GET'])
def get_song_list():
    room_id = request.args.get('id')
    room = rooms.get(room_id)
    if room:
        return jsonify({"queue": room.get("queue", [])})
    else:
        return jsonify({"error": "Room not found"}), 404

# TEST  
if __name__ == "__main__":
    app.run(debug=True, port=5000)