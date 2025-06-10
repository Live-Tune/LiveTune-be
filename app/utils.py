from flask import jsonify
import time
from threading import Thread
from .logger_config import get_logger

TTL_SECONDS = 3600 * 12  # 12 hour

logger = get_logger(__name__) 

def find_room(rooms: dict, id: int):
    """
    Finds a room by its id in the rooms dictionary
    Returns the room object if found, None if not
    """
    if id in rooms:
        return rooms.get(id)
    
def find_user(users: dict, id):
    """
    Finds a user by its id in the users dictionary
    """

    if id in users:
        return users.get(id)
    
def is_user_in_room(rooms, uid):
    """
    Checks if user is in a room
    """
    for room in rooms.values():
        if uid in room.current_users:
            return True
    return False
    
def cleanup_inactive_users(users, rooms):
    """
    Finds and deletes users that has not been in a room for 1 hour or more
    """
    now = time.time()

    expired_uids = []

    for uid, user in list(users.items()):
        if not is_user_in_room(rooms, uid) and (now - user.last_active) > TTL_SECONDS:
            expired_uids.append(uid)

    for uid in expired_uids:
        logger.info(f"Removing inactive user: {users[uid].username}")
        del users[uid]

def start_cleanup(users, rooms):
    def run():
        while True:
            logger.info("Starting user cleanup process")
            cleanup_inactive_users(users, rooms)
            time.sleep(TTL_SECONDS)
    Thread(target=run, daemon=True).start()