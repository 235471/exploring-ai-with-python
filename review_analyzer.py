"""
Review analysis utilities.
Uses AI to analyze product reviews for sentiment and categories.
"""
import re
import pandas as pd
from google import genai
from groq import Groq
import prompts
from ai_utils import ask_gemini, ask_groq


def ai_analyze_reviews(df: pd.DataFrame, client, analysis_type: str) -> pd.DataFrame:
    """Generic review analyzer using configurations from prompts.AI_PROMPTS.
    
    Args:
        df: DataFrame with a 'reviewText' column.
        client: Gemini or Groq client.
        analysis_type: Key from prompts.AI_PROMPTS (e.g., 'feelings', 'categories').
    
    Returns:
        DataFrame with the new analysis column added.
    """
    if analysis_type not in prompts.AI_PROMPTS:
        print(f"Error: Unknown analysis type '{analysis_type}'. Available: {list(prompts.AI_PROMPTS.keys())}")
        return df
    
    config = prompts.AI_PROMPTS[analysis_type]
    
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


def ai_evalution_of_feelings(df: pd.DataFrame, client) -> pd.DataFrame:
    """Evaluates the feelings of users based on the product reviews.
    
    Convenience wrapper for backwards compatibility.
    
    Args:
        df: DataFrame with 'reviewText' column.
        client: AI client (Gemini or Groq).
        
    Returns:
        DataFrame with 'feeling' column added.
    """
    return ai_analyze_reviews(df, client, "feelings")


def ai_identify_negative_categories(df: pd.DataFrame, client) -> pd.DataFrame:
    """Identifies general categories for negative reviews.
    
    Convenience wrapper for backwards compatibility.
    
    Args:
        df: DataFrame with 'reviewText' column.
        client: AI client (Gemini or Groq).
        
    Returns:
        DataFrame with 'category' column added.
    """
    return ai_analyze_reviews(df, client, "categories")
