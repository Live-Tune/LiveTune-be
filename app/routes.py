# REST API endpoints
from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.classes import Room
from app.utils import *

from . import rooms, users
next_room_id = 1 # id is just a counter now

api_bp = Blueprint('api', __name__, url_prefix='/api') 
# this is so that we can "attach" the routes to the app instance
# defined in __init__. 

## -- ROOMS -- 

# Create room
@api_bp.route("/room/createnew", methods=["POST"])
def createroom():
    
    global next_room_id

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    rooms[next_room_id] = Room(data, id=next_room_id)
    next_room_id += 1

    print("Room created successfully.") # testing purposes
    return jsonify({"id": (next_room_id - 1)}), 201


# Update room settings
@api_bp.route("/room/updatesettings", methods=["PUT"])
def updatesettings():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    try:
        id = int(data.get('id'))
    except ValueError:
        return jsonify({"error": "Room id ('id') must be an integer"}), 400

    room_to_update = find_room(rooms, id) # Use find_room for consistency
    if room_to_update is None:
        return jsonify({"error": "Room not found"}), 404

    rooms[id].update_settings(data)

    print("Room updated successfully.") # testing purposes
    return jsonify({"message": "Room updated successfully"}), 200

# Retrieve available public rooms
@api_bp.route("/room/availablepublicrooms", methods=["GET"])
def getpublicrooms():

    public_rooms_data = []
    for room_id, room_obj in rooms.items():
        if not room_obj.is_private:
            # 일단 I will return the whole object but I think we should
            # only return a couple properties
            public_rooms_data.append(room_obj.to_dict())

    return jsonify(public_rooms_data), 200

# Deleting a room
@api_bp.route("/room/deleteroom", methods=["DELETE"])
def deleteroom():

    try:
        id = int(request.args.get('id'))
    except ValueError:
        return jsonify({"message": "Query parameter 'id' must be an integer"}), 400

    if find_room(rooms, id) is not None:
        del rooms[id]
        return jsonify({"message": "Room deleted successfully"}), 200
    else:
        return jsonify({"message": "Room not found"}), 404

# Retrieving id from room name
@api_bp.route("/room/getid", methods=['GET']) 
def get_room_id():           
    name = request.args.get('name')
    for room_id, room_obj in rooms.items():
        if room_obj.name == name:
            return jsonify({"id": room_id})
    
    return jsonify({"error": "Room not found"}), 404

# Retrieve room info
@api_bp.route("/room/info", methods=['GET'])
def get_room_info():
    
    try:
        id = int(request.args.get('id'))
    except (ValueError, TypeError):
        return jsonify({"error": "Query parameter 'id' must be an integer"}), 400

    room = find_room(rooms, id)
    
    room_data = room.to_dict()
    if room_data:
        filtered = {
            "name": room_data.get("name"),
            "description": room_data.get("description"),
            "current_users_number": len(room_data.get("currentUsers", [])),
            "host": room_data.get("host"),
        }
        return jsonify(filtered), 200
    
# Retrieve room's playlist
@api_bp.route("/room/songlist", methods=['GET'])
def get_song_list():

    try:
        id = int(request.args.get('id'))
    except (ValueError, TypeError):
        return jsonify({"error": "Query parameter 'id' must be an integer"}), 400

    room = find_room(rooms, id)

    room_data = room.to_dict()

    return jsonify(room_data.get("queue")), 200