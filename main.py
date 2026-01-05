"""
Main entry point for AI experiments.
Contains example usage of all modules.
"""
from pathlib import Path
import pandas as pd

# Import all modules
from clients import get_gemini_client, get_groq_client
from ai_utils import ask_gemini, ask_groq, chat_bot
from file_utils import read_txt_files, save_txt_files, read_csv, save_to_csv
from email_utils import summarize_emails, execute_batch_email_generation, execute_individual_email_generation
from review_analyzer import ai_evalution_of_feelings, ai_identify_negative_categories
from data_transform import df_filter_by, translate_to_english
from challenge_utils import execute_challenge
from qa_generator import generate_qa_pair_in_batch

BASE_DIR = Path(__file__).parent


def main():
    """Main function with example usage."""
    
    # Initialize clients
    client_gemini = get_gemini_client()
    client_groq = get_groq_client()
    
    # Different models with less quota:
    # model_name = "gemini-flash-latest"
    # model_name = "gemini-3-flash-preview"    
    # model_name = "gemini-2-flash-preview"

    # ============================================
    # Example 1: Simple Question
    # ============================================
    # question = "What's the color of the sky?"
    # answer = ask_gemini(client_gemini, question)
    # print(f"Gemini Answer: {answer}")

    # ============================================
    # Example 2: Chat Session
    # ============================================
    # history = chat_bot(client_gemini)
    # print(f"Chat history: {history}")

    # ============================================
    # Example 3: Email Summarization
    # ============================================
    # Traditional way (1 by 1)
    # emails = execute_individual_email_generation(client_gemini, 5)
    
    # New efficient batch way
    # emails = execute_batch_email_generation(client_gemini, 5)
    # Save emails in .txt files
    # save_txt_files(emails, "emails.txt", "\n\n--- EMAIL ---\n\n")
    # summarized_emails = summarize_emails(client_gemini, emails)
    # save_txt_files(summarized_emails, "summarized_emails.txt", "\n")

    # ============================================
    # Example 4: Groq
    # ============================================
    # answer = ask_groq(client_groq, "What's the difference between electron and proton?")
    # print(answer)

    # ============================================
    # Example 5: CSV Reading
    # ============================================
    # df = read_csv(BASE_DIR / "meu_csv.csv")
    # print(df.head())
    # print(df.tail())

    # ============================================
    # Example 6: Q&A Generation and CSV save
    # ============================================
    # questions, answers, dict_q_a = generate_qa_pair_in_batch(client_gemini, count=5)
    # save_txt_files(questions, "questions.txt")
    # save_txt_files(answers, "answers.txt")
    # if questions and answers:
    #     save_to_csv("results.csv", questions=questions, answers=answers)
        # Verify the save
        # df_new = pd.read_csv(BASE_DIR / "results.csv")
        # print("\nReviewing saved CSV (from lists):")
        # print(df_new.head())
        
    #     # Save Q&A pairs to CSV using the dictionary list
        # save_to_csv("qa_pairs.csv", data=dict_q_a)
        # df_qa = pd.read_csv(BASE_DIR / "qa_pairs.csv")
        # print("\nReviewing saved Q&A pairs (from dict list):")
        # print(df_qa.head())

    # ============================================
    # Example 7: DataFrame Manipulation
    # ============================================
    df = read_csv(BASE_DIR / "produtos.csv")
    
    # Filtering examples:
    # filtered_df = df_filter_by(df, "`Categoria do Produto` == 'Eletrônicos'")
    # print(filtered_df)
    # filtered_df = df_filter_by(df, "`Avaliação do Produto` > 4.6")
    # print(filtered_df)
    # filtered_df = df_filter_by(df, "`Categoria do Produto` == 'Eletrônicos' and `Avaliação do Produto` > 4.6")
    # print(filtered_df)

    # Translation example:
    # df_cat = df.set_index("Categoria do Produto")
    # df_final = translate_to_english(df_cat)
    # save_to_csv("products.csv", data=df_final)

    # ============================================
    # Example 8: Review Sentiment Analysis
    # ============================================
    # df_eval = read_csv(BASE_DIR / "reviews.csv")
    # df_eval_filtered = df_eval[0:][["reviewText"]]
    # df_eval_with_feelings = ai_evalution_of_feelings(df_eval_filtered, client_gemini)
    # df_eval["reviewFeeling"] = df_eval_with_feelings["feeling"]
    # save_to_csv("reviews_with_feelings.csv", data=df_eval)

    # ============================================
    # Example 9: Negative Review Categories
    # ============================================
    # df_complaints = read_csv(BASE_DIR / "reviews_with_feelings.csv")
    # df_negative_reviews = df_complaints[df_complaints["reviewFeeling"] == "negative"][["reviewText"]].copy()
    # df_negative_reviews_with_categories = ai_identify_negative_categories(df_negative_reviews, client_groq)
    # print("\nNegative reviews with identified categories:")
    # print(df_negative_reviews_with_categories)
    
    # ============================================
    # Example 10: Challenge Execution
    # ============================================
    summary, formatted_str = execute_challenge(client_gemini)

    print("\n--- Challenge Result ---")
    print(f"Counts: {summary}")
    print("\nFormatted Data:")
    print(formatted_str)


if __name__ == "__main__":
    main()
