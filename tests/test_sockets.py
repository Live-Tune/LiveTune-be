import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, socketio, rooms, users, sid_user_map
from app.classes import User, Room

@pytest.fixture
def app_instance():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app_instance):
    return app_instance.test_client()

@pytest.fixture
def socketio_client(app_instance, client): # client fixture is needed for context
    return socketio.test_client(app_instance, flask_test_client=client)

@pytest.fixture(autouse=True)
def clean_state():
    """Clears global state before and after each test."""
    rooms.clear()
    users.clear()
    sid_user_map.clear()
    yield
    rooms.clear()
    users.clear()
    sid_user_map.clear()

def test_on_join_room(socketio_client):
    # Setup initial state if necessary
    test_user_id = "test_user_123"
    test_room_id = 1
    
    users[test_user_id] = User(username="Test User", uid=test_user_id)
    rooms[test_room_id] = Room(data={
        "name": "Test Room",
        "is_private": False,
        "description": "A room for testing",
        "max_user": 10,
        "host": test_user_id # Assuming host is a user ID
    }, id=test_room_id)
    # Simulate client connecting (optional, but good practice)
    socketio_client.connect()

    # Emit the 'join_room' event
    socketio_client.emit("join_room", {"room_id": str(test_room_id), "user": test_user_id})

    # Assertions
    # 1. Check if the user was added to the room's current_users list
    assert test_user_id in rooms[test_room_id].current_users

    # 2. Check if 'user_joined' event was broadcasted
    received = socketio_client.get_received()
    
    # Find the 'user_joined' event
    user_joined_event = None
    for msg in received:
        if msg['name'] == 'user_joined':
            user_joined_event = msg
            break
    
    assert user_joined_event is not None
    assert user_joined_event['args'][0]['user'] == test_user_id
    # Note: Flask-SocketIO's test client captures broadcasts to rooms the test client itself is in.
    # The on_join handler calls flask_socketio.join_room(room_id), so the client is in the room.

    socketio_client.disconnect()

def test_on_connect(socketio_client):
    # The test client connects automatically on creation (connect_on_start=True default)
    assert socketio_client.is_connected()

    # Test explicit disconnect
    socketio_client.disconnect()
    assert not socketio_client.is_connected()

    # Test explicit connect (reconnect)
    socketio_client.connect()
    assert socketio_client.is_connected()

    # The on_connect handler on the server primarily logs; direct assertion of log is out of scope here.
    socketio_client.disconnect() # Clean up for this test

def test_on_disconnect_cleans_user_from_room(socketio_client):
    test_user_id = "user_disconnect_test"
    test_room_id = 101

    users[test_user_id] = User(username="Disconnect User", uid=test_user_id)
    rooms[test_room_id] = Room(data={
        "name": "Disconnect Room", "is_private": False, "description": "Test",
        "max_user": 5, "host": test_user_id
    }, id=test_room_id)
    
    socketio_client.connect()
    # Simulate user joining the room to populate sid_user_map and room.current_users
    socketio_client.emit("join_room", {"room_id": str(test_room_id), "user": test_user_id})
    _ = socketio_client.get_received() # Clear join messages

    assert test_user_id in rooms[test_room_id].current_users
    client_sid = next((sid for sid, uid in sid_user_map.items() if uid == test_user_id), None)
    assert client_sid is not None

    socketio_client.disconnect() # This triggers on_disconnect on the server

    assert client_sid not in sid_user_map
    # After disconnect, if the user was the last one, the room is deleted.
    # Room should be deleted as it becomes empty
    assert test_room_id not in rooms

def test_on_disconnect_no_user_mapping(socketio_client):
    socketio_client.connect()
    # SID exists, but not in sid_user_map for this test
    # Store a copy of rooms to ensure no unexpected room deletions
    initial_rooms_keys = list(rooms.keys())

    socketio_client.disconnect() # Triggers on_disconnect

    # Assert that no errors occurred and sid_user_map is not unexpectedly changed for other sids
    # and no rooms were deleted if they weren't related to this SID.
    assert all(key in rooms for key in initial_rooms_keys) # No unrelated rooms deleted

def test_on_leave_room_cleans_user_and_room_if_empty(socketio_client):
    test_user_id = "user_leave_test"
    test_room_id = 202

    users[test_user_id] = User(username="Leave User", uid=test_user_id)
    rooms[test_room_id] = Room(data={
        "name": "Leave Room", "is_private": False, "description": "Test",
        "max_user": 5, "host": test_user_id
    }, id=test_room_id)

    socketio_client.connect()
    socketio_client.emit("join_room", {"room_id": str(test_room_id), "user": test_user_id})
    _ = socketio_client.get_received() # Clear join messages

    assert test_user_id in rooms[test_room_id].current_users

    socketio_client.emit("leave_room", {"room_id": str(test_room_id), "user": test_user_id})

    # The user should be removed. If they were the last one, the room is deleted.
    # The check `assert test_room_id not in rooms` later will confirm deletion.
    received = socketio_client.get_received()
    # The client that emitted "leave_room" results in `leave_room(room_id)` being called
    # on the server for its own SID. Thus, it should not receive the "user_left" event
    # subsequently broadcast to that room.
    user_left_event = next((msg for msg in received if msg['name'] == 'user_left'), None)
    assert user_left_event is None

    # Room should be deleted as it becomes empty
    assert test_room_id not in rooms

    socketio_client.disconnect()

def test_send_message_type_msg(socketio_client):
    test_user_id = "user_msg_test"
    test_room_id = 303
    test_message_content = "Hello LiveTune!"

    users[test_user_id] = User(username="Msg User", uid=test_user_id)
    rooms[test_room_id] = Room(data={
        "name": "Msg Room", "is_private": False, "description": "Test",
        "max_user": 5, "host": test_user_id
    }, id=test_room_id)

    socketio_client.connect()
    socketio_client.emit("join_room", {"room_id": str(test_room_id), "user": test_user_id})
    _ = socketio_client.get_received()

    socketio_client.emit("send_message", {
        "room_id": str(test_room_id), "message_type": "msg", "message": test_message_content
    })

    received = socketio_client.get_received()
    msg_event = next((m for m in received if m['name'] == 'receive_message'), None)
    assert msg_event is not None
    assert msg_event['args'][0]['message'] == test_message_content
    socketio_client.disconnect()

def test_send_message_type_play_or_pause(socketio_client):
    test_user_id = "user_control_test"
    test_room_id = 404

    users[test_user_id] = User(username="Control User", uid=test_user_id)
    rooms[test_room_id] = Room(data={
        "name": "Control Room", "is_private": False, "description": "Test",
        "max_user": 5, "host": test_user_id
    }, id=test_room_id)

    socketio_client.connect()
    socketio_client.emit("join_room", {"room_id": str(test_room_id), "user": test_user_id})
    _ = socketio_client.get_received()

    # Test "play"
    socketio_client.emit("send_message", {"room_id": str(test_room_id), "message_type": "play"})
    received_play = socketio_client.get_received()
    # include_self=False, so sender should not receive "broadcast_play"
    assert not any(m['name'] == 'broadcast_play' for m in received_play)

    # Test "pause"
    socketio_client.emit("send_message", {"room_id": str(test_room_id), "message_type": "pause"})
    received_pause = socketio_client.get_received()
    # include_self=False, so sender should not receive "broadcast_pause"
    assert not any(m['name'] == 'broadcast_pause' for m in received_pause)

    socketio_client.disconnect()

def test_send_message_type_ping(socketio_client):
    socketio_client.connect()
    _ = socketio_client.get_received() # Clear any connection messages

    # room_id is technically sent but not used by the server for 'ping' target
    socketio_client.emit("send_message", {"room_id": "0", "message_type": "ping"})

    received = socketio_client.get_received()
    pong_event = next((m for m in received if m['name'] == 'pong'), None)
    assert pong_event is not None
    assert pong_event['args'][0] == {} # Expecting an empty dict
    socketio_client.disconnect()
