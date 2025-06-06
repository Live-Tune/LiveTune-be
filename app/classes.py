class Room:

    def __init__(self, data, id):

        self.name = data["name"]
        self.is_private = data["is_private"]
        self.description = data["description"]
        self.max_user = data["max_user"]
        self.host = data["host"]  
        self.id = id
        self.current_users = []
        self.queue = []
        self.current_song = None
    
    def update_settings(self, data):

        self.name = data["name"]
        self.description = data["description"]
        self.max_user = data["max_user"]
        self.host = data["host"] 
    
    def to_dict(self):
        return {
            "name": self.name,
            "isPrivate": self.is_private,
            "description": self.description,
            "max_user": self.max_user,
            "current_users": self.current_users,
            "host": self.host,
            "queue": self.queue,
            "id": self.id,
            "current_song": self.current_song
        }
    
    def add_user(self, user_id):
        self.current_users.append(user_id)

    def remove_user(self, user_id):
        self.current_users.remove(user_id)

class Song: 

    def __init__(self, title, youtube_id, added_by):
        self.title = title
        self.youtube_id = youtube_id
        self.added_by = added_by

class User:

    def __init__(self, username, uid):
        self.username = username
        self.uid = uid

    def to_dict(self):
        return {
            "username": self.username,
            "uid": self.uid
        }

    def update_username(self, username):
        self.username = username