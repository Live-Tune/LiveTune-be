# REST API endpoints

from flask import Flask, Blueprint, request, jsonify
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
    room_id = len(rooms) + 1
   
    rooms[next_room_id] = Room(name=room_name, isprivate=is_room_private, description=room_description, maxUser=room_maxUser, host=room_host, ID=next_room_id)
    next_room_id += 1

    return "Room created successfully.", 201

# TEST  
if __name__ == "__main__":
    app.run(debug=True, port=5000)