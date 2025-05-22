class Room:

    def __init__(self, name, isprivate, description, maxUser, host, ID):
        self.name = name
        self.isprivate = isprivate
        self.description = description
        self.maxUser = maxUser
        self.host = host
        self.ID = ID
    
    def update_settings(self, new_room_name, new_room_description, new_room_maxUser, new_room_host):
        self.name = new_room_name
        self.description = new_room_description
        self.maxUser = new_room_maxUser
        self.host = new_room_host
    
    def to_dict(self):
        return {
            "name": self.name,
            "isprivate": self.isprivate,
            "description": self.description,
            "maxUser": self.maxUser,
            "host": self.host,
            "ID": self.ID
        }