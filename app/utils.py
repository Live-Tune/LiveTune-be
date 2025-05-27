from flask import jsonify

def find_room(rooms: dict, ID: int):
    """
    Finds a room by its ID in the rooms dictionary
    Returns the room object if found, None if not
    """
    if ID in rooms:
        return rooms.get(ID)