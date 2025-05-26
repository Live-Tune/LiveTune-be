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

    rooms[next_room_id] = Room(data, ID=next_room_id)
    next_room_id += 1

    print("Room created successfully.") # testing purposes
    return jsonify({"message": "Room created successfully"}), 201


# Update room settings
@app.route("/api/room/updatesettings", methods=["PUT"])
def updatesettings():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    ID = data.get('ID')
    if int(ID) not in rooms:
        return jsonify({"error": "Room not found"}), 404

    rooms[ID].update_settings(data)

    print("Room updated successfully.") # testing purposes
    return jsonify({"message": "Room updated successfully"}), 201

# Retrieve available public rooms
@app.route("/api/room/availablepublicrooms", methods=["GET"])
def getpublicrooms():

    public_rooms_data = []
    for room_id, room_obj in rooms.items():
        if not room_obj.is_private:
            # 일단 I will return the whole object but I think we should
            # only return a couple properties
            public_rooms_data.append(room_obj.to_dict())

    return jsonify(public_rooms_data), 200

# Deleting a room
@app.route("/api/room/deleteroom", methods=["DELETE"])
def deleteroom():

    ID = int(request.args.get('ID'))

    if ID in rooms:
        del rooms[ID]
        print("Room deleted successfully.") # testing purposes
        return jsonify({"message": "Room deleted successfully"}), 201
    else:
        return "Room not found.", 404

# Retrieving ID from room name
@app.route('/api/room/getid', methods=['GET']) 
def get_room_id():           
    name = request.args.get('name')
    for room_id, room_obj in rooms.items():
        if room_obj.name == name:
            return jsonify({"ID": room_id})
    
    return jsonify({"error": "Room not found"}), 404

# Retrieve room info
@app.route('/api/room/info', methods=['GET'])
def get_room_info():
    
    try:
        ID = int(request.args.get('ID'))
    except (ValueError, TypeError):
        return jsonify({"error": "Query parameter 'ID' must be an integer"}), 400

    if ID in rooms:
        room = rooms[ID]
    else:
        return jsonify({"error": "Room not found"}), 404

    room_data = room.to_dict()
    if room_data:
        filtered = {
            "name": room_data["name"],
            "description": room_data["description"],
            "current_users_number": len(room_data.get("currentUsers")),
            "host": room_data["host"],
        }
        return jsonify(filtered), 200
    
# Retrieve room's playlist
@app.route('/api/room/songlist', methods=['GET'])
def get_song_list():

    try:
        ID = int(request.args.get('ID'))
    except (ValueError, TypeError):
        return jsonify({"error": "Query parameter 'ID' must be an integer"}), 400

    if ID in rooms:
        room = rooms[ID]
    else:
        return jsonify({"error": "Room not found"}), 404  

    room_data = room.to_dict()
    if room_data:
        return jsonify(room_data.get("queue")), 200
    else:
        return jsonify({"error": "Room not found"}), 404

# TEST  
if __name__ == "__main__":
    app.run(debug=True, port=5000)