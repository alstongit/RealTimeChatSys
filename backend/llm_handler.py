import httpx
import os
import json

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "mistral")


# This function now becomes an async generator
async def generate_response_stream(prompt: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True  # The key change is here!
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Use stream() to get a streaming response
            async with client.stream("POST", OLLAMA_API_URL, json=payload) as response:
                response.raise_for_status()
                # Read the streaming response line by line
                async for line in response.aiter_lines():
                    if line:
                        try:
                            # Each line is a JSON object
                            data = json.loads(line)
                            # Yield the actual text chunk
                            yield data.get("response", "")
                            # Check if the stream is done
                            if data.get("done"):
                                break
                        except json.JSONDecodeError:
                            print(f"[LLM WARNING] Failed to decode JSON line: {line}")


    except httpx.RequestError as e:
        print(f"[LLM ERROR] Request failed: {e}")
        yield "⚠️ Failed to reach the local LLM. Is Ollama running?"

    except httpx.HTTPStatusError as e:
        print(f"[LLM ERROR] HTTP error: {e.response.status_code} - {e.response.text}")
        yield "⚠️ LLM returned an error."

    except Exception as e:
        print(f"[LLM ERROR] Unexpected error: {str(e)}")
        yield "⚠️ Unexpected error when calling the LLM."