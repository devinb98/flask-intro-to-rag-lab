from __future__ import annotations

import requests

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"


def generate_response(prompt: str) -> str:
    """Send a prompt to Ollama and return the generated text."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json=payload,
            timeout=90,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure Ollama is installed, running, "
            "and that the llama3.2 model has been pulled."
        ) from error
    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "The Ollama request timed out. Try again or use a shorter prompt."
        ) from error
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Ollama request failed: {error}") from error
    except ValueError as error:
        raise RuntimeError("Ollama returned invalid JSON.") from error

    generated_text = data.get("response", "").strip()

    if not generated_text:
        raise RuntimeError("Ollama returned an empty response.")

    return generated_text
