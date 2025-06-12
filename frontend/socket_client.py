import socketio
import threading
from queue import Queue
import time
import os

# Create a background Socket.IO client
sio = socketio.Client(reconnection_attempts=5, reconnection_delay=2)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
# Thread-safe queue to hold incoming bot responses
bot_message_queue = Queue()

def connect_to_server():
    """Tries to connect to the server in a loop."""
    while not sio.connected:
        try:
            print(f"[SocketClient] Attempting to connect to {BACKEND_URL}...")
            # Use the correct socketio_path that matches the server
            sio.connect(BACKEND_URL, socketio_path="/ws/socket.io")
        except socketio.exceptions.ConnectionError as e:
            print(f"[SocketClient] Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

@sio.event
def connect():
    print("[SocketClient] Connected to backend")

@sio.event
def disconnect():
    print("[SocketClient] Disconnected from backend")

@sio.on("bot_response")
def on_bot_response(data):
    """
    Handles incoming messages from the server and puts them in the queue.
    The data is a dictionary, e.g., {'type': 'chunk', 'content': 'hello'}
    """
    # print(f"[SocketClient] Received: {data}")
    bot_message_queue.put(data)

def send_user_message(message: str):
    if sio.connected:
        sio.emit("user_message", {"message": message})

def get_bot_response():
    """Non-blocking fetch of bot response from queue"""
    if not bot_message_queue.empty():
        return bot_message_queue.get_nowait()
    return None

# Connect in a separate thread to avoid blocking Streamlit
def start_socket_client():
    # Check if a thread is already running
    if "socket_thread" not in globals() or not globals()["socket_thread"].is_alive():
        print("[SocketClient] Starting connection thread...")
        globals()["socket_thread"] = threading.Thread(target=connect_to_server, daemon=True)
        globals()["socket_thread"].start()