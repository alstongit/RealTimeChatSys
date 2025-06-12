import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from socket_manager import register_socketio_events

# Create a new Async Socket.IO server
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

# Create FastAPI app
app = FastAPI()

# Enable CORS for frontend to connect via WebSocket
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wrap the FastAPI app with Socket.IO's ASGI app
# Explicitly set the path to avoid ambiguity between client/server versions
socket_app = socketio.ASGIApp(sio, other_asgi_app=app, socketio_path="/ws/socket.io")

# Register all socket events
register_socketio_events(sio)