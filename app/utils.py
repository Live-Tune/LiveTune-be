from flask import jsonify

def find_room(rooms: dict, ID: int):
    if ID in rooms:
        return rooms[ID]
    else:
        return jsonify({"error": "Room not found"}), 404  