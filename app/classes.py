class Room:

    def __init__(self, data, id):

        self.name = data["name"]
        self.is_private = data["is_private"]
        self.description = data["description"]
        self.max_user = data["max_user"]
        self.host = data["host"]  
        self.id = id
        self.currentUsers = []
        self.queue = []
    
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
            "currentUsers": self.currentUsers,
            "host": self.host,
            "queue": self.queue,
            "id": self.id
        }
    
class Song: 

    def __init__(self, title, youtube_id, added_by):
        self.title = title
        self.youtube_id = youtube_id
        self.added_by = added_by