import os
import time
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
        return None

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

def summarize_emails(client, email_list):  
    if not email_list:
        print("No emails to summarize.")
        return

    try:
        for i, mail in enumerate(email_list):
            if not mail:
                print("Skipping empty email...")
                continue
                
            prompt = "Summarize in a single line what this email is about:\n" + mail
            response = ask_gemini(client, prompt)
            
            if response:
                print(f"Email {i+1} Summary: {response.strip()}")
            else:
                print("Failed to get summary for this email.")
            
            print("-" * 60)
            # Wait a bit to avoid hitting free tier rate limits
            time.sleep(2)
    except Exception as e:
        print(f"Error in summarize_emails: {e}")

def execute_individual_email_generation(client, count=20):
    answer = []
    print("Generating simulated emails...")
    for i in range(count):
        question = 'Write a believable email message of any given subject, avoid the content being too long or short'
        result = ask_gemini(client, question)
        if result:
            answer.append(result)
            print(f"Generated email {i+1}/{count}")
        else:
            print(f"Failed to generate email {i+1}")
        
        # Rate limit mitigation
        time.sleep(2)
        
    return answer

def execute_batch_email_generation(client, count=20):
    print(f"Generating {count} simulated emails in a single batch...")
    
    delimiter = "===EMAIL_SEP==="
    prompt = f"""Generate {count} believable email messages of any given subject. 
    Separate each email with the unique delimiter '{delimiter}'. 
    Avoid the content being too long or short.
    Do not include any preamble, introduction, or conclusion text - only the emails and delimiters."""
    
    result = ask_gemini(client, prompt)
    
    if not result:
        print("Failed to generate batch emails.")
        return []
    
    # Split the result by the delimiter and clean up each email
    emails = [email.strip() for email in result.split(delimiter) if email.strip()]
    
    print(f"Successfully generated {len(emails)} emails.")
    return emails

if __name__ == "__main__":
    client = get_gemini_client()
# Different models with less quota
    # model_name = "gemini-flash-latest"
    # model_name = "gemini-3-flash-preview"    
    # model_name = "gemini-2-flash-preview"

    # Example 1: Simple Question
    # question = "What's the color of the sky?"
    # answer = ask_gemini(client, question)
    # print(f"Gemini Answer: {answer}")

    # Example 2: Chat Session
    # Get chat history
    # history = chat_bot(client)
    # print(f"Chat history: {history}")

    # Example 3: Email Summarization
    # Traditional way (1 by 1)
    # answer = execute_email_summarization(client)
    
    # New efficient batch way
    emails = execute_batch_email_generation(client, 5)
    print(emails)
    summarize_emails(client, emails)