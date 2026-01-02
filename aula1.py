import os
import time
from google import genai
from dotenv import load_dotenv
from groq import Groq
from pathlib import Path
import pandas as pd
from typing import List, Dict, Sequence, Any
import mapping
import re
import json
from collections import Counter

BASE_DIR = Path(__file__).parent

load_dotenv()

def get_gemini_client():
    api_key_gemini = os.getenv("GEMINI_API_KEY")
    if not api_key_gemini:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    client = genai.Client(api_key=api_key_gemini)
    return client

def get_groq_client():
    api_key_groq = os.getenv("GROQ_API_KEY")
    if not api_key_groq:
        raise ValueError("GROQ_API_KEY not found in .env file")
    
    client = Groq(api_key=api_key_groq)
    return client   

def ask_gemini(client, question, model_name="gemma-3-27b-it"):
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

def ask_groq(client, prompt, model="llama-3.3-70b-versatile"):
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
    summary = []  
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
                summary.append(f"Email {i+1} Summary: {response.strip()}")
            else:
                print("Failed to get summary for this email.")
            # Wait a bit to avoid hitting free tier rate limits
            time.sleep(2)
    except Exception as e:
        print(f"Error in summarize_emails: {e}")
    return summary
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

def save_txt_files(raw_data, file_name, separator="\n"):
    if not raw_data:
        print("No data to save.")
        return
    
    if isinstance(raw_data, list):
        content = separator.join(str(item).strip() for item in raw_data if item)
    else:
        content = str(raw_data).strip()
    
    with open(BASE_DIR / file_name, "w", encoding="utf-8") as f:
        f.write(content + "\n" if content else "")

def read_txt_files(file_name):
    encodings = ['utf-8', 'latin-1', 'windows-1252', 'iso-8859-1']    
    content = None
    
    for encoding in encodings:
        try:
            with open(BASE_DIR / file_name, "r", encoding=encoding) as f:
                content = f.read()
                break
        except UnicodeDecodeError:
            continue
    
    if not content:
        raise ValueError("Failed to decode file with any of the specified encodings.")
    
    return content.split("\n")

def read_csv(file_name):
    return pd.read_csv(file_name)     

def save_to_csv(file_name, questions=None, answers=None, data=None):
    """
    Saves data to a CSV file. 
    Accepts either separate 'questions' and 'answers' lists, 
    or a 'data' object (like a list of dictionaries).
    """
    if data is not None:
        df = pd.DataFrame(data)
    elif questions is not None and answers is not None:
        if len(questions) != len(answers):
            print("Warning: Questions and answers lists have different lengths!")
            min_len = min(len(questions), len(answers))
            questions = questions[:min_len]
            answers = answers[:min_len]
        
        df = pd.DataFrame({
            'Question': questions,
            'Answer': answers
        })
    else:
        print("Error: No data provided to save_to_csv.")
        return

    df.to_csv(BASE_DIR / file_name, index=False, sep=',', encoding='utf-8')
    print(f"Successfully saved to {file_name}")

def generate_qa_pair_in_batch(client, count=10) -> tuple[List[str], List[str], List[Dict[str, str]]]:
    print(f"Generating {count} Q&A pairs in a single batch...")
    
    q_delimiter = "===QUESTION_SEP==="
    pair_delimiter = "===PAIR_SEP==="
    
    prompt = f"""Generate {count} questions and their respective answers.
    Follow these rules:
    - For each pair, provide the question first, then the answer.
    - Separate the question and answer with '{q_delimiter}'.
    - Separate each Q&A pair with '{pair_delimiter}'.
    - The questions should be clear and concise.
    - The questions should be challenging and thought-provoking.
    - The questions should be related to the topic.
    - The questions should be open-ended.
    - The questions should be specific and focused.
    - The answers should be clear and concise while providing a complete and accurate response.
    - Do not include any preamble, introduction, or conclusion text.
    
    Format example:
    Question text {q_delimiter} Answer text {pair_delimiter} Next question {q_delimiter} Next answer ...
    """
    
    result = ask_gemini(client, prompt)
    
    if not result:
        print("Failed to generate batch Q&A.")
        return [], []
    
    questions = []
    answers = []
    dict_q_a = []
    
    pairs = [pair.strip() for pair in result.split(pair_delimiter) if pair.strip()]
    for pair in pairs:
        if q_delimiter in pair:
            parts = pair.split(q_delimiter)
            questions.append(parts[0].strip())
            answers.append(parts[1].strip())
            dict_q_a.append({"Question": parts[0].strip(), "Answer": parts[1].strip()})
            
    print(f"Successfully generated {len(questions)} Q&A pairs (lists + dict list).")
    return questions, answers, dict_q_a

def df_filter_by(df: pd.DataFrame, query_string: str) -> pd.DataFrame:
    """Filters a DataFrame using a query string.
    
    Args:
        df (pd.DataFrame): The DataFrame to filter.
        query_string (str): The query expression to apply.
    
    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    try:
        return df.query(query_string)
    except Exception as e:
        print(f"Error during query '{query_string}': {e}")
        return df

def translate_to_english(df: pd.DataFrame) -> pd.DataFrame:
    """Translates the DataFrame to English using mapping."""
    df_final = (
        df
        .rename(index={"Eletrônicos": "Electronics", "Móveis": "Furniture", "Roupas": "Clothing", "Eletrodomésticos": "Appliances"})
        .reset_index()
        .rename(columns={
            "Categoria do Produto": "Category",
            "Nome do Produto": "Name",
            "Preço do produto": "Price",
            "Quantidade do produto que foram vendidas": "Quantity",
            "Avaliação do Produto": "Rating"
        })
    )

    mask = df_final["Name"].isin(mapping.mapper.keys())
    df_final.loc[mask, "Name"] = df_final.loc[mask, "Name"].map(mapping.mapper)
    return df_final

def ai_analyze_reviews(df: pd.DataFrame, client, analysis_type: str) -> pd.DataFrame:
    """Generic review analyzer using configurations from mapping.AI_PROMPTS.
    
    Args:
        df: DataFrame with a 'reviewText' column
        client: Gemini or Groq client
        analysis_type: Key from mapping.AI_PROMPTS (e.g., 'feelings', 'categories')
    
    Returns:
        DataFrame with the new analysis column added
    """
    if analysis_type not in mapping.AI_PROMPTS:
        print(f"Error: Unknown analysis type '{analysis_type}'. Available: {list(mapping.AI_PROMPTS.keys())}")
        return df
    
    config = mapping.AI_PROMPTS[analysis_type]
    
    if df.empty:
        print(f"Error: No data provided for '{analysis_type}' analysis.")
        return df

    try:
        # Build numbered review list
        reviews_numbered = ""
        for i, review in enumerate(df["reviewText"], 1):
            reviews_numbered += f"{i}. {review}\n"
        
        # Format prompt with count and reviews
        prompt = config["prompt"].format(count=len(df), reviews=reviews_numbered)
        
        # Call appropriate AI client
        result = None
        if isinstance(client, genai.Client):
            result = ask_gemini(client, prompt)
        elif isinstance(client, Groq):
            result = ask_groq(client, prompt)
        else:
            print("Error: Unknown client type.")
            return df
        
        if result:
            pattern = re.compile(config["regex"], re.IGNORECASE)
            matches = pattern.findall(result)
            
            if len(matches) == len(df):
                df[config["column"]] = matches
            else:
                print(f"Warning: Received {len(matches)} results for {len(df)} reviews. Mismatch occurred.")
                print("Raw output from model:")
                print(result)
        
        return df
        
    except Exception as e:
        print(f"Error during '{analysis_type}' analysis: {e}")
        return df


# Convenience wrappers for backwards compatibility
def ai_evalution_of_feelings(df: pd.DataFrame, client) -> pd.DataFrame:
    """Evaluates the feelings of users based on the product reviews."""
    return ai_analyze_reviews(df, client, "feelings")


def ai_identify_negative_categories(df: pd.DataFrame, client) -> pd.DataFrame:
    """Identifies general categories for negative reviews."""
    return ai_analyze_reviews(df, client, "categories")    

def execute_challenge(client):
    challenge_list = read_txt_files("challenge.txt")
    size = len(challenge_list)
    challenge_list = "\n".join(challenge_list)
    json_output_example = """
    [
        {
            "username": "username",
            "original review": "original review",
            "translated review": "translated review",
            "feeling": "positive"
        }
    ]
    """
    prompt = f"""
        Each line has 3 fields userId, username and review.
        They are separated by the delimiter $.
        It has '{size} lines to be processed.
        The current list of reviews is:
        {challenge_list}
        Extract the fields username, original review. Then add a new field translated review to english, analyze the review and add a column feeling of the review which you need to classify as[positive, negative, neutral].
        Return the result in json format and no other text.
        Example:
        {json_output_example}
    """
    response = ask_gemini(client, prompt)    
    
    if not response:
        print("Failed to get a response from the AI.")
        return None, None

    # Clean the response in case it contains markdown code blocks
    if response.strip().startswith("```"):
        response = re.sub(r"^```json\n|```$", "", response, flags=re.MULTILINE).strip()
    
    try:
        dict_output = json.loads(response)
        summary, formatted_str = format_output(dict_output)

        return summary, formatted_str
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Raw response was:")
        print(response)
        return None, None

def format_output(dict_output):

    counts = Counter(item["feeling"] for item in dict_output)

    string_raw = "===SEP===".join(
         str(item.get("username", "")) + str(item.get("original review", "")) + str(item.get("translated review", "")) + str(item.get("feeling", ""))
        for item in dict_output
    )

    return dict(counts), string_raw

if __name__ == "__main__":
    client_gemini = get_gemini_client()
    client_groq = get_groq_client()
# Different models with less quota
    # model_name = "gemini-flash-latest"
    # model_name = "gemini-3-flash-preview"    
    # model_name = "gemini-2-flash-preview"

    # Example 1: Simple Question
    # question = "What's the color of the sky?"
    # answer = ask_gemini(client_gemini, question)
    # print(f"Gemini Answer: {answer}")

    # Example 2: Chat Session
    # Get chat history
    # history = chat_bot(client_gemini)
    # print(f"Chat history: {history}")

    # Example 3: Email Summarization
    # Traditional way (1 by 1)
    # answer = execute_email_summarization(client_gemini)
    
    # New efficient batch way
    # emails = execute_batch_email_generation(client_gemini, 5)
    # Save emails and summaries in .txt files
    # save_emails(emails, "emails.txt", "\n\n--- EMAIL ---\n\n")
    # summarized_emails =summarize_emails(client_gemini, emails)
    # save_emails(summarized_emails, "summarized_emails.txt", "\n")

    # Example 4: Groq
    # answer = ask_groq(client_groq,"What's the difference between electron and proton?")
    # print(answer)

    # Example 5: CSV
    # df = read_csv("meu_csv.csv")
    # print(df.head())
    # print(df.tail())

    # Example 6: Optimized Single-Prompt Generation and CSV save
    # questions, answers, dict_q_a = generate_qa_pair_in_batch(client_gemini, count=5)
    # save_txt_files(questions, "questions.txt")
    # save_txt_files(answers, "answers.txt")
    # if questions and answers:
    #     save_to_csv("results.csv", questions=questions, answers=answers)
    #     # Verify the save
    #     df_new = pd.read_csv(BASE_DIR / "results.csv")
    #     print("\nReviewing saved CSV (from lists):")
    #     print(df_new.head())
        
    #     # Example 7: Save Q&A pairs to CSV using the dictionary list
    #     save_to_csv("qa_pairs.csv", data=dict_q_a)
    #     # Verify the save
    #     df_qa = pd.read_csv(BASE_DIR / "qa_pairs.csv")
    #     print("\nReviewing saved Q&A pairs (from dict list):")
    #     print(df_qa.head())

    # Example 8: Manipulating CSV
    df = read_csv(BASE_DIR / "produtos.csv")
    # Returns the number of rows and columns
    # print(df.shape)

    # returns the category name and the number of times each value appears 
    # print(df['Categoria do Produto'].value_counts())
    # returns the number of unique values
    # print(df['Categoria do Produto'].nunique())
    # returns the unique values
    # print(df['Categoria do Produto'].unique())
    # returns the unique values as a set(dictionary)
    # print(set(df['Categoria do Produto']))

    # Filtering by
    # filtered_df = df_filter_by(df, "`Categoria do Produto` == 'Eletrônicos'")
    # print(filtered_df)
    # filtered_df = df_filter_by(df, "`Avaliação do Produto` > 4.6")
    # print(filtered_df)
    # filtered_df = df_filter_by(df, "`Categoria do Produto` == 'Eletrônicos' and `Avaliação do Produto` > 4.6")
    # print(filtered_df)

    # ILOC
    # print(df.iloc[0])
    # print(df.iloc[:5])
    # print(df.iloc[30:])
    # print(df.iloc[-5:])

    #LOC
    # df_cat = df.set_index("Categoria do Produto")
    # print(df_cat.loc["Eletrônicos"])
    # print(df_cat.loc["Eletrônicos", ["Nome do Produto", "Preço do produto"]])
    # print(df_cat.loc["Eletrônicos", ["Nome do Produto", "Preço do produto"]].values)
    # print(df_cat.loc["Eletrônicos", ["Nome do Produto", "Preço do produto"]].values[0])
    # print(df_cat.loc[["Eletrônicos", "Móveis"], ["Nome do Produto", "Preço do produto"]])
    # mask = (df_cat.index.isin(["Eletrônicos", "Móveis"])) & (df_cat["Avaliação do Produto"] > 4.6)
    # print(df_cat.loc[mask, ["Nome do Produto", "Avaliação do Produto"]])

    # df_final = translate_to_english(df_cat)
    # save_to_csv("products.csv", data=df_final)

    # Example 9: CSV Manipulation, adding column and evaluating feelings of the users with AI
    # df_eval = read_csv(BASE_DIR / "reviews.csv")
    # df_eval_filtered = df_eval[0:][["reviewText"]]
    # df_eval_with_feelings = ai_evalution_of_feelings(df_eval_filtered, client_gemini)
    # df_eval["reviewFeeling"] = df_eval_with_feelings["feeling"]
    # save_to_csv("reviews_with_feelings.csv", data=df_eval)

    # Example 10: CSV Manipulation, evaluate and create categories of the complaints when the review is negative
    # df_complaints = read_csv(BASE_DIR / "reviews_with_feelings.csv")
    # df_negative_reviews = df_complaints[df_complaints["reviewFeeling"] == "negative"][["reviewText"]].copy()
    # df_negative_reviews_with_categories = ai_identify_negative_categories(df_negative_reviews, client_groq)
    # print("\nNegative reviews with identified categories:")
    # print(df_negative_reviews_with_categories)
    
    summary, formatted_str = execute_challenge(client_gemini)

    print("\n--- Challenge Result ---")
    print(f"Counts: {summary}")
    print("\nFormatted Data:")
    print(formatted_str)