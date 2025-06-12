import streamlit as st
import time
from socket_client import start_socket_client, send_user_message, get_bot_response

st.set_page_config(page_title="Real-Time Chatbot", page_icon="💬", layout="wide")

# --- Session State Initialization ---
# This ensures that the state is preserved across re-runs
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_streaming" not in st.session_state:
    st.session_state.is_streaming = False

# --- Socket Connection ---
# Use a flag in session_state to ensure the connection thread starts only once.
if "socket_started" not in st.session_state:
    start_socket_client()
    st.session_state.socket_started = True
    # Give the socket a moment to connect on first load
    time.sleep(1) 
    # Get the initial welcome message from the bot
    initial_message = get_bot_response()
    if initial_message and initial_message.get("type") == "full_message":
         st.session_state.messages.append({"role": "assistant", "content": initial_message.get("content")})

# --- UI Rendering ---
st.title("🤖 Real-Time Chat with LLM")

# Display all past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle User Input ---
if prompt := st.chat_input("Ask something...", disabled=st.session_state.is_streaming):
    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send message to the backend and activate streaming mode
    send_user_message(prompt)
    st.session_state.is_streaming = True
    st.rerun() # Re-run to enter the polling loop immediately

# --- Real-time Streaming and Polling Logic ---
if st.session_state.is_streaming:
    # Create a placeholder for the streaming response
    with st.chat_message("assistant"):
        placeholder = st.empty()

    full_response = ""
    # Loop to continuously check the queue for new chunks
    while st.session_state.is_streaming:
        response_item = get_bot_response()
        
        if response_item:
            # Handle different message types from the backend
            if response_item.get("type") == "chunk":
                full_response += response_item.get("content", "")
                placeholder.markdown(full_response + " ▌") # Show a blinking cursor
            
            elif response_item.get("type") == "end_of_stream":
                # Finalize the message and exit the loop
                placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                st.session_state.is_streaming = False
                st.rerun() # Rerun one last time to clear the placeholder logic
                break # Exit the while loop
            
            elif response_item.get("type") == "error":
                # Handle server-side errors
                error_message = response_item.get("content", "An unknown error occurred.")
                placeholder.error(error_message)
                st.session_state.is_streaming = False
                break

        # Wait a fraction of a second before polling again to prevent high CPU usage
        time.sleep(0.05)