"""
Utility script to list available Gemini models.
"""
from clients import get_gemini_client


def list_available_models():
    """Lists all available models from the Gemini API."""
    client = get_gemini_client()
    
    print("Available Models:")
    for model in client.models.list():
        print(f" - {model.name}")


if __name__ == "__main__":
    list_available_models()
