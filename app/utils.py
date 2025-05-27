from flask import jsonify

def find_room(rooms: dict, id: int):
    """
    Finds a room by its id in the rooms dictionary
    Returns the room object if found, None if not
    """
    if id in rooms:
        return rooms.get(id)