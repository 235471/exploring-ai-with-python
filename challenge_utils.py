"""
Challenge-specific utilities.
Functions for the review processing challenge.
"""
import re
import json
from collections import Counter
from google import genai
from ai_utils import ask_gemini
from file_utils import read_txt_files


def execute_challenge(client: genai.Client) -> tuple[dict | None, str | None]:
    """Executes the review processing challenge.
    
    Reads reviews from file, uses AI to extract details,
    translate, and determine sentiment.
    
    Args:
        client: Configured Gemini client.
        
    Returns:
        Tuple of (sentiment_counts, formatted_string) or (None, None) on error.
    """
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


def format_output(dict_output: list[dict]) -> tuple[dict, str]:
    """Formats the challenge output.
    
    Counts sentiment occurrences and creates a formatted string.
    
    Args:
        dict_output: List of dictionaries with review data.
        
    Returns:
        Tuple of (sentiment_counts_dict, formatted_string).
    """
    counts = Counter(item["feeling"] for item in dict_output)

    string_raw = "===SEP===".join(
         str(item.get("username", "")) + str(item.get("original review", "")) + str(item.get("translated review", "")) + str(item.get("feeling", ""))
        for item in dict_output
    )

    return dict(counts), string_raw
