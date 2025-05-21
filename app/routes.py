from flask import Flask, jsonify, request
app = Flask(__name__)

rooms = {}

@app.route('/api/room/getid', methods=['GET']) 
def get_room_id():           
    room_title = request.args.get('title')
    for room_id, room_data in rooms.items():
        if room_data.get("title") == room_title:
            return jsonify({"id": room_id})
    
    return jsonify({"error": "Room not found"}), 404
    
@app.route('/api/room/info', methods=['GET'])
def get_room_info():
    room_id = request.args.get('id')
    room = rooms.get(room_id)
    if room:
        filtered = {
            "title": room.get("title"),
            "description": room.get("description"),
            "currentUsers": room.get("currentUsers")
        }
        return jsonify(filtered)
    else:
        return jsonify({"error": "Room not found"}), 404
    
@app.route('/api/room/songlist', methods=['GET'])
def get_song_list():
    room_id = request.args.get('id')
    room = rooms.get(room_id)
    if room:
        return jsonify({"queue": room.get("queue", [])})
    else:
        return jsonify({"error": "Room not found"}), 404


if __name__ == "__main__":
    app.run()