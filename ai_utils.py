"""
Core AI interaction utilities.
Contains functions for making AI API calls and chat functionality.
"""
from google import genai
from groq import Groq


def ask_gemini(client: genai.Client, question: str, model_name: str = "gemma-3-27b-it") -> str | None:
    """Sends a question to Gemini and returns the response.
    
    Args:
        client: Configured Gemini client.
        question: The prompt/question to send.
        model_name: Model to use (default: gemma-3-27b-it).
        
    Returns:
        The model's response text, or None on error.
    """
    print("Calling Gemini with model:", model_name)
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=question
        )
        return response.text   
    except Exception as e:
        print(f"Error during Gemini call: {e}")
        return None


def ask_groq(client: Groq, prompt: str, model: str = "llama-3.3-70b-versatile") -> str | None:
    """Sends a prompt to Groq and returns the response.
    
    Args:
        client: Configured Groq client.
        prompt: The prompt to send.
        model: Model to use (default: llama-3.3-70b-versatile).
        
    Returns:
        The model's response text, or None on error.
    """
    try:
        print(f"Calling Groq with model: {model}")
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=4000,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error during Groq call: {e}")
        return None


def create_chat_gemini(client: genai.Client, model_name: str = "gemma-3-27b-it"):
    """Creates a Gemini chat session.
    
    Args:
        client: Configured Gemini client.
        model_name: Model to use for chat.
        
    Returns:
        Chat session object.
    """
    try:
        chat = client.chats.create(model=model_name)
        return chat
    except Exception as e:
        print(f"Error during Gemini call: {e}")
        return None


def chat_bot(client: genai.Client) -> list:
    """Interactive chat bot using Gemini.
    
    Args:
        client: Configured Gemini client.
        
    Returns:
        Chat history as a list.
    """
    try:
        chat = create_chat_gemini(client)
        if not chat:
            return []
            
        while True:
            prompt = input("Type in your question (or 'exit' to quit): ").strip()
            
            # Check for exit or empty input
            if not prompt or prompt.lower() == "exit":
                break
                
            answer_chat = chat.send_message(prompt).text
            print(f"Chat: {answer_chat}")
            print("\n")
            
        # Get and return chat history
        return chat.get_history()
    except Exception as e:
        print(f"Error in chat_bot: {e}")
        return []
