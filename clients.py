"""
AI Client initialization module.
Handles creation of Gemini and Groq API clients.
"""
import os
from google import genai
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


def get_gemini_client() -> genai.Client:
    """Creates and returns a configured Gemini client.
    
    Returns:
        genai.Client: Configured Gemini API client.
        
    Raises:
        ValueError: If GEMINI_API_KEY is not found in environment.
    """
    api_key_gemini = os.getenv("GEMINI_API_KEY")
    if not api_key_gemini:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    client = genai.Client(api_key=api_key_gemini)
    return client


def get_groq_client() -> Groq:
    """Creates and returns a configured Groq client.
    
    Returns:
        Groq: Configured Groq API client.
        
    Raises:
        ValueError: If GROQ_API_KEY is not found in environment.
    """
    api_key_groq = os.getenv("GROQ_API_KEY")
    if not api_key_groq:
        raise ValueError("GROQ_API_KEY not found in .env file")
    
    client = Groq(api_key=api_key_groq)
    return client
