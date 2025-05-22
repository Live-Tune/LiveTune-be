class Room:

    def __init__(self, name, isPrivate, description, maxUser, host, ID):
        self.name = name
        self.isPrivate = isPrivate
        self.description = description
        self.maxUser = maxUser
        self.currentUsers = []
        self.host = host
        self.ID = ID
        self.queue = []
    
    def update_settings(self, new_room_name, new_room_description, new_room_maxUser, new_room_host):
        self.name = new_room_name
        self.description = new_room_description
        self.maxUser = new_room_maxUser
        self.host = new_room_host
    
    def to_dict(self):
        return {
            "name": self.name,
            "isPrivate": self.isPrivate,
            "description": self.description,
            "maxUser": self.maxUser,
            "currentUsers": self.currentUsers,
            "host": self.host,
            "queue": self.queue,
            "ID": self.ID
        }
    
class Song: 

    def __init__(self, title, youtube_id, added_by):
        self.title = title
        self.youtube_id = youtube_id
        self.added_by = added_by