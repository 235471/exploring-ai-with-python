"""
Email generation and summarization utilities.
"""
import time
from google import genai
from ai_utils import ask_gemini


def summarize_emails(client: genai.Client, email_list: list[str]) -> list[str]:
    """Summarizes a list of emails using AI.
    
    Args:
        client: Configured Gemini client.
        email_list: List of email contents to summarize.
        
    Returns:
        List of email summaries.
    """
    summary = []  
    if not email_list:
        print("No emails to summarize.")
        return summary

    try:
        for i, mail in enumerate(email_list):
            if not mail:
                print("Skipping empty email...")
                continue
                
            prompt = "Summarize in a single line what this email is about:\n" + mail
            response = ask_gemini(client, prompt)
            
            if response:
                summary.append(f"Email {i+1} Summary: {response.strip()}")
            else:
                print("Failed to get summary for this email.")
            # Wait a bit to avoid hitting free tier rate limits
            time.sleep(2)
    except Exception as e:
        print(f"Error in summarize_emails: {e}")
    return summary


def execute_individual_email_generation(client: genai.Client, count: int = 20) -> list[str]:
    """Generates emails one by one.
    
    Args:
        client: Configured Gemini client.
        count: Number of emails to generate.
        
    Returns:
        List of generated emails.
    """
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


def execute_batch_email_generation(client: genai.Client, count: int = 20) -> list[str]:
    """Generates multiple emails in a single API call.
    
    More efficient than individual generation for large counts.
    
    Args:
        client: Configured Gemini client.
        count: Number of emails to generate.
        
    Returns:
        List of generated emails.
    """
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
