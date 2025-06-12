from socketio import AsyncServer
# Import the new streaming function
from llm_handler import generate_response_stream

def register_socketio_events(sio: AsyncServer):

    @sio.event
    async def connect(sid, environ):
        print(f"[Socket] Client connected: {sid}")
        # Let's send a more structured response
        await sio.emit("bot_response", {"type": "full_message", "content": "👋 Hello! Ask me anything."}, to=sid)

    @sio.event
    async def disconnect(sid):
        print(f"[Socket] Client disconnected: {sid}")

    @sio.event
    async def user_message(sid, data):
        print(f"[Socket] Message from {sid}: {data}")

        user_input = data.get("message", "")
        if not user_input.strip():
            await sio.emit("bot_response", {"type": "full_message", "content": "❗ Please enter a valid message."}, to=sid)
            return

        # Use the new streaming function
        # We will stream chunks back to the client
        try:
            async for chunk in generate_response_stream(user_input):
                if chunk: # Ensure we don't send empty chunks
                    await sio.emit("bot_response", {"type": "chunk", "content": chunk}, to=sid)
            
            # After the loop finishes, send an end-of-stream signal
            await sio.emit("bot_response", {"type": "end_of_stream"}, to=sid)

        except Exception as e:
            print(f"[Socket ERROR] Error during streaming: {e}")
            await sio.emit("bot_response", {"type": "error", "content": "An error occurred on the server."}, to=sid)