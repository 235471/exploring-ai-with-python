# AI Integration & Exploration with Python

This project demonstrates how to integrate various AI models (Google Gemini and Groq) into a Python application. It explores capabilities such as sentiment analysis, email summarization, Q&A generation, and chatbot interactions, all structured in a modular and scalable way.

## 🚀 Features

-   **Multi-Model Support**: Seamlessly switch between Google Gemini and Groq (Llama, etc.).
-   **Review Analysis**: Analyze product reviews for customer sentiment (Positive, Neural, Negative).
-   **Email Automation**: Generate realistic test emails and summarize existing ones using AI.
-   **Data Transformation**: detailed tools for processing text files and CSVs, including translating content.
-   **Chatbot**: A terminal-based interactive chat interface.
-   **Q&A Generation**: Automatically create Question & Answer pairs for datasets or testing.

## 📂 Project Structure

The project is organized into modular components for better maintainability:

| File | Purpose |
|------|---------|
| `main.py` | **Entry point**. Contains examples of how to run all features. |
| `clients.py` | Configuration and initialization of AI clients (Gemini & Groq). |
| `ai_utils.py` | Core wrapper functions for API interactions. |
| `review_analyzer.py` | specialized logic for analyzing text and reviews. |
| `email_utils.py` | Tools to generate and summarize emails. |
| `qa_generator.py` | Utilities for generating Q&A pairs in batch. |
| `file_utils.py` | Helpers for reading/writing CSV and TXT files. |
| `prompts.py` | Centralized storage for AI prompts and data mappings. |

## 🛠️ Prerequisites

-   Python 3.10+
-   A Google Gemini API Key
-   A Groq API Key

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    
    # On Windows:
    .\venv\Scripts\activate
    
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```ini
    GEMINI_API_KEY=your_gemini_api_key_here
    GROQ_API_KEY=your_groq_api_key_here
    ```

## ▶️ Usage

The project is designed to be explored via the `main.py` file. Open it to see various examples commented out. Uncomment the specific example you want to run.

To run the main script:

```bash
python main.py
```

### Examples included in `main.py`:
-   **Simple Question**: Ask a single question to an AI model.
-   **Chat Session**: Start an interactive chat loop.
-   **Email Summarization**: Generate dummy emails and summarize them.
-   **CSV Processing**: Read, filter, and translate CSV datasets.
-   **Review Analysis**: Process a list of reviews to detect sentiment.
-   **Challenge**: Run the full review processing challenge pipeline.

## 🧪 Testing

You can verify that your environment is set up correctly (without making API calls) by running the import tests:

```bash
python -c "from clients import get_gemini_client; print('Setup OK')"
```

To list available Gemini models:
```bash
python list_models.py
```

## 📝 License

This project is for educational purposes.
