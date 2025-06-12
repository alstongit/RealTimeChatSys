# Real-Time LLM Chat Application

This project is a fully containerized, real-time chat application that allows users to interact with a local Large Language Model (LLM) powered by [Ollama](https://ollama.com/). The system uses a FastAPI/Socket.IO backend for asynchronous messaging and a Streamlit frontend for the user interface.

The entire application is orchestrated with Docker Compose, making setup and deployment incredibly simple.

  <!-- Optional: Replace with a screenshot of your app! -->

## Features

-   **Real-Time Streaming:** Responses from the LLM are streamed back to the user token-by-token, providing an interactive, real-time experience.
-   **Local LLM:** Utilizes Ollama to run powerful open-source models (like Mistral, Llama 2, etc.) entirely on your own machine. Your data stays private.
-   **Multi-User Support:** Built with Socket.IO and Streamlit sessions to handle multiple concurrent users with isolated, private conversations.
-   **Fully Dockerized:** The entire stack (frontend, backend, and LLM) is defined in `docker-compose.yml` for one-command setup.
-   **Asynchronous Backend:** Built with FastAPI and `python-socketio` for high-performance, non-blocking communication.

## Tech Stack

-   **Backend:** FastAPI, Python-SocketIO, Uvicorn
-   **Frontend:** Streamlit
-   **LLM Service:** Ollama
-   **Containerization:** Docker & Docker Compose

## Prerequisites

-   [Docker](https://www.docker.com/get-started/) installed and running on your system.
-   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop).
-   Sufficient RAM to run the desired LLM (e.g., ~8 GB for a 7B parameter model).

## 🚀 Getting Started

Follow these steps to get the application running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
```

### 2. Build and Run the Services

Use Docker Compose to build the images and start all the containers in the background.

```bash
docker-compose up --build -d
```

-   `--build`: Forces a rebuild of the images to ensure your latest code is used.
-   `-d`: Runs the containers in detached mode.

### 3. Download an LLM Model

The first time you run the application, the Ollama service will be empty. You need to tell it which model to download. The default model for this application is `mistral`.

Open a new terminal and run the following command to execute `ollama pull` inside the running `ollama` container:

```bash
docker exec -it ollama ollama pull mistral
```

*(You can replace `mistral` with another model like `llama2` or `codellama`, but you'll need to update the `OLLAMA_MODEL` environment variable in `llm_handler.py` if you do.)*

You will see the model download progress in your terminal. This only needs to be done once, as the model will be persisted in a Docker volume.

### 4. Access the Application

Once the model is downloaded, your chat application is ready!

Open your web browser and navigate to:

**[http://localhost:8501](http://localhost:8501)**

You should be greeted by the chatbot interface, ready to accept your prompts.

## Managing the Application

-   **To view live logs** from all services:
    ```bash
    docker-compose logs -f
    ```

-   **To stop the application:**
    ```bash
    docker-compose down
    ```
    *(Your downloaded Ollama models will be preserved in the `ollama-data` volume.)*

-   **To restart the application** after stopping it:
    ```bash
    docker-compose up -d
    ```

## Project Structure

```
.
├── backend/         # FastAPI and Socket.IO server
├── frontend/        # Streamlit UI
├── .gitignore       # Files to ignore for Git
├── docker-compose.yml # Defines all services and networks
└── README.md        # This file
```