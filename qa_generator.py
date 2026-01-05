"""
Question & Answer generation utilities.
"""
from typing import List, Dict
from google import genai
from ai_utils import ask_gemini


def generate_qa_pair_in_batch(client: genai.Client, count: int = 10) -> tuple[List[str], List[str], List[Dict[str, str]]]:
    """Generates Q&A pairs in a single batch API call.
    
    Args:
        client: Configured Gemini client.
        count: Number of Q&A pairs to generate.
        
    Returns:
        Tuple containing:
        - List of questions
        - List of answers  
        - List of dictionaries with Question/Answer keys
    """
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
        return [], [], []
    
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
