"""
File I/O utilities.
Handles reading and writing text and CSV files.
"""
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent


def save_txt_files(raw_data, file_name: str, separator: str = "\n") -> None:
    """Saves data to a text file.
    
    Args:
        raw_data: Data to save (can be a list or string).
        file_name: Name of the file to save to.
        separator: Separator between list items (default: newline).
    """
    if not raw_data:
        print("No data to save.")
        return
    
    if isinstance(raw_data, list):
        content = separator.join(str(item).strip() for item in raw_data if item)
    else:
        content = str(raw_data).strip()
    
    with open(BASE_DIR / file_name, "w", encoding="utf-8") as f:
        f.write(content + "\n" if content else "")


def read_txt_files(file_name: str) -> list[str]:
    """Reads a text file and returns its lines.
    
    Tries multiple encodings for compatibility.
    
    Args:
        file_name: Name of the file to read.
        
    Returns:
        List of lines from the file.
        
    Raises:
        ValueError: If file cannot be decoded with any encoding.
    """
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


def read_csv(file_name: str) -> pd.DataFrame:
    """Reads a CSV file into a DataFrame.
    
    Args:
        file_name: Path to the CSV file.
        
    Returns:
        DataFrame containing the CSV data.
    """
    return pd.read_csv(file_name)     


def save_to_csv(file_name: str, questions: list = None, answers: list = None, data=None) -> None:
    """Saves data to a CSV file.
    
    Accepts either separate 'questions' and 'answers' lists, 
    or a 'data' object (like a list of dictionaries).
    
    Args:
        file_name: Name of the file to save to.
        questions: Optional list of questions.
        answers: Optional list of answers.
        data: Optional data object (e.g., list of dicts).
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
