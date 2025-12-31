import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    client = genai.Client(api_key=api_key)
    return client

def ask_gemini(client, question, model_name="gemma-3-27b-it"):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=question
        )
        return response.text   
    except Exception as e:
        print(f"Error during Gemini call: {e}")

def create_chat_gemini(client, model_name="gemma-3-27b-it"):
    try:
        chat = client.chats.create(model=model_name)
        return chat
    except Exception as e:
        print(f"Error during Gemini call: {e}")

def chat_bot(client):
    try:
        chat = create_chat_gemini(client)
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

if __name__ == "__main__":
    client = get_gemini_client()
# Different models with less quota
    # model_name = "gemini-flash-latest"
    # model_name = "gemini-3-flash-preview"    
    # model_name = "gemini-2-flash-preview"

    # Example 1: Simple Question
    # question = "What color is the sky?"
    # answer = ask_gemini(client, question)
    # print(f"Gemini Answer: {answer}")

    # Example 2: Chat Session
    # Get chat history
    history = chat_bot(client)
    # print(f"Chat history: {history}")